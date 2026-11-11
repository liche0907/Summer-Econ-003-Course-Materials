<#
  MergeAll.ps1 - join the numbered parts 1.mp4, 2.mp4, ... into one lecture.

    .\MergeAll.ps1                              1..7  -> Lecture_Full.mp4
    .\MergeAll.ps1 -Count 5                     1..5
    .\MergeAll.ps1 -Count 7 -Out Ch03_full.mp4  custom output name

  Two passes, both lossless - nothing is re-encoded.

  Pass 1 normalises every part into _merge_tmp\, forcing video to stream 0 and
  audio to stream 1 with a common time scale. This matters: Zoom writes some
  recordings audio-first, and the concat demuxer matches streams by POSITION,
  not by type. Feed it a mixed set and it pushes video packets into the audio
  track, which is what produces "Non-monotonic DTS" and an output several times
  longer than the sum of its parts.

  Pass 2 concatenates the normalised copies and checks the result against the
  expected running time.
#>
param(
  [int]$Count = 7,
  [string]$Out = 'Lecture_Full.mp4',
  [string]$Ext = 'mp4',
  [switch]$KeepTemp
)

$ErrorActionPreference = 'Stop'
$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

# ---- locate ffmpeg: beside this script -> a build folder under it -> PATH.
# A "shared" build must run from its own bin folder so Windows finds its DLLs,
# so point at it in place rather than copying the exe out.
function Find-Tool([string]$name) {
  $direct = Join-Path $root $name
  if (Test-Path $direct) {
    $dlls = @(Get-ChildItem -Path $root -Filter '*.dll' -ErrorAction SilentlyContinue)
    $nested = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
              ForEach-Object { Get-ChildItem -Path $_.FullName -Recurse -Filter $name -ErrorAction SilentlyContinue } |
              Select-Object -First 1
    if ($dlls.Count -gt 0 -or -not $nested) { return $direct }
    return $nested.FullName
  }
  $found = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
           ForEach-Object { Get-ChildItem -Path $_.FullName -Recurse -Filter $name -ErrorAction SilentlyContinue } |
           Select-Object -First 1
  if ($found) { return $found.FullName }
  $onPath = Get-Command ($name -replace '\.exe$', '') -ErrorAction SilentlyContinue
  if ($onPath) { return $onPath.Source }
  throw "Could not find $name. Put it beside this script, or on PATH."
}

$FFMPEG  = Find-Tool 'ffmpeg.exe'
$FFPROBE = Find-Tool 'ffprobe.exe'
$LOG     = Join-Path $root 'ffmpeg_log.txt'

# ffmpeg writes warnings to stderr even on a clean run, and PowerShell turns a
# native program's stderr into error records - under 'Stop' that aborts the
# script on a harmless warning. Run it detached with stderr sent to a file and
# judge the run by its exit code instead.
function Invoke-FF([string[]]$ffArgs, [string]$what) {
  $quoted = $ffArgs | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }
  Remove-Item $LOG -ErrorAction SilentlyContinue
  $p = Start-Process -FilePath $FFMPEG -ArgumentList $quoted -NoNewWindow -Wait -PassThru -RedirectStandardError $LOG
  $notes = @()
  if (Test-Path $LOG) { $notes = @(Get-Content $LOG | Where-Object { $_.Trim() -ne '' }) }
  if ($p.ExitCode -ne 0) {
    Write-Host ''
    Write-Host ("ffmpeg failed while " + $what + ". It said:") -ForegroundColor Red
    if ($notes.Count -eq 0) { Write-Host '  (nothing)' } else { $notes | ForEach-Object { Write-Host "  $_" } }
    throw ("ffmpeg exited with code " + $p.ExitCode + ".")
  }
  Remove-Item $LOG -ErrorAction SilentlyContinue
  return $notes
}

function Probe-Duration([string]$file) {
  $raw = & $FFPROBE -v error -show_entries format=duration -of csv=p=0 $file
  $val = 0.0
  [void][double]::TryParse(("$raw").Trim(), [ref]$val)
  return $val
}

function Show-Time([double]$sec) {
  return ('{0}:{1:00}' -f [int][math]::Floor($sec / 60), [int][math]::Floor($sec % 60))
}

Write-Host ("using: " + $FFMPEG) -ForegroundColor DarkGray

# ---- collect 1..Count in order
$Parts = @(); $missing = @()
foreach ($i in 1..$Count) {
  $f = Join-Path $root ("{0}.{1}" -f $i, $Ext)
  if (Test-Path $f) { $Parts += $f } else { $missing += ("{0}.{1}" -f $i, $Ext) }
}
if ($missing.Count -gt 0) {
  throw ("Missing in this folder: " + ($missing -join ', ') + ". Rename the parts, or pass -Count.")
}
if ($Parts.Count -lt 2) { throw 'Need at least two parts to join.' }

$OutFull = Join-Path $root $Out
if ($Parts -contains $OutFull) { throw "Output name collides with a part: $Out" }

# ---- running order, expected total, and a note on which parts are audio-first
Write-Host 'Joining, in this order:'
$total = 0.0
foreach ($p in $Parts) {
  $d = Probe-Duration $p
  $total += $d
  $order = (& $FFPROBE -v error -show_entries stream=codec_type -of csv=p=0 $p) -join ','
  $flag = if ($order -notmatch '^video') { '   (audio-first - will be reordered)' } else { '' }
  Write-Host ('  {0,-10} {1}{2}' -f (Split-Path $p -Leaf), (Show-Time $d), $flag)
}
Write-Host ('  {0,-10} {1}' -f '= total', (Show-Time $total)) -ForegroundColor DarkGray

# ---- pass 1: normalise
$tmp = Join-Path $root '_merge_tmp'
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
New-Item -ItemType Directory -Path $tmp | Out-Null

Write-Host ''
Write-Host 'Pass 1 - normalising parts...' -ForegroundColor DarkGray
$norm = @()
for ($i = 0; $i -lt $Parts.Count; $i++) {
  $dst = Join-Path $tmp ("n{0}.mp4" -f ($i + 1))
  Invoke-FF @('-hide_banner', '-nostdin', '-loglevel', 'error', '-y',
              '-i', $Parts[$i],
              '-map', '0:v:0', '-map', '0:a:0', '-c', 'copy',
              '-video_track_timescale', '90000', $dst) ("normalising " + (Split-Path $Parts[$i] -Leaf)) | Out-Null
  $norm += $dst
  Write-Host ('  ok  ' + (Split-Path $Parts[$i] -Leaf)) -ForegroundColor DarkGray
}

# ---- pass 2: concatenate. Forward slashes only - the demuxer treats \ as an
# escape character, so Windows paths fail with "No such file or directory".
$list = Join-Path $tmp 'concat_list.txt'
$norm | ForEach-Object { "file '" + ($_ -replace '\\', '/') + "'" } | Set-Content -Path $list -Encoding ASCII

Write-Host 'Pass 2 - merging...' -ForegroundColor DarkGray
$notes = Invoke-FF @('-hide_banner', '-nostdin', '-loglevel', 'warning', '-y',
                     '-f', 'concat', '-safe', '0', '-i', $list,
                     '-c', 'copy', '-movflags', '+faststart', $OutFull) 'merging'

if ($notes.Count -gt 0) {
  Write-Host 'ffmpeg warnings - the merge still finished:' -ForegroundColor DarkYellow
  $notes | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
}
if (-not (Test-Path $OutFull)) { throw "ffmpeg reported success but $Out is not there." }

# ---- check the result before throwing the temporaries away
$d  = Probe-Duration $OutFull
$mb = (Get-Item $OutFull).Length / 1MB
$off = [math]::Abs($d - $total)

Write-Host ''
if ($off -gt 2) {
  Write-Host ('{0}  ->  {1}  ({2:N1} MB)' -f $Out, (Show-Time $d), $mb) -ForegroundColor Red
  Write-Warning ('Expected {0}, got {1}. Something is wrong - keeping {2} so you can look.' -f (Show-Time $total), (Show-Time $d), $tmp)
} else {
  Write-Host ('{0}  ->  {1}  ({2:N1} MB)' -f $Out, (Show-Time $d), $mb) -ForegroundColor Green
  Write-Host ('matches the expected {0}' -f (Show-Time $total)) -ForegroundColor DarkGray
  if (-not $KeepTemp) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
}
