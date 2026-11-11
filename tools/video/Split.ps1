<#
  Split.ps1 - cut one recording into two halves at a single point, losslessly.

    .\Split.ps1 "W3\Chapter 6.mp4" -At 76:16
    .\Split.ps1 "W3\Chapter 6.mp4" -At 76:16 -OutA "W3\Ch6 part1.mp4" -OutB "W3\Ch6 part2.mp4"

  Times accept  SS  |  MM:SS  |  HH:MM:SS.
  Defaults to <name>_a.mp4 and <name>_b.mp4 beside the input.

  Nothing is re-encoded, so both halves are bit-for-bit the original.

  NOTHING IS EVER REPEATED. The first half ends exactly where you asked. The
  second half can only begin on a keyframe, so it begins on the first keyframe
  at or AFTER your split point - never before it. That way the tail never opens
  by replaying the end of the first half. The script prints how much sits in the
  gap between them (usually a frame or two of transition) and warns if that gap
  is big enough to contain real content.
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$In,
  [Parameter(Mandatory=$true)][string]$At,
  [string]$OutA,
  [string]$OutB
)

$ErrorActionPreference = 'Stop'
$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

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

function ConvertTo-Seconds([string]$t) {
  $p = $t.Split(':')
  switch ($p.Count) {
    1 { [double]$p[0] }
    2 { [double]$p[0] * 60 + [double]$p[1] }
    3 { [double]$p[0] * 3600 + [double]$p[1] * 60 + [double]$p[2] }
    default { throw "Cannot read the time '$t'. Use SS, MM:SS or HH:MM:SS." }
  }
}

function Show-Time([double]$sec) {
  return ('{0}:{1:00.00}' -f [int][math]::Floor($sec / 60), ($sec % 60))
}

function Probe-Duration([string]$file) {
  $raw = & $FFPROBE -v error -show_entries format=duration -of csv=p=0 $file
  $val = 0.0
  [void][double]::TryParse(("$raw").Trim(), [ref]$val)
  return $val
}

function Get-Keyframes([string]$file, [double]$from, [double]$to) {
  $raw = @(& $FFPROBE -v error -select_streams v:0 -skip_frame nokey `
             -show_entries frame=pts_time -of csv=p=0 `
             -read_intervals ("{0}%{1}" -f [math]::Max(0, $from), $to) $file)
  $out = @()
  foreach ($line in $raw) {
    $s = ("$line" -replace '[^0-9\.\-]', '')
    if ($s -ne '') { $v = 0.0; if ([double]::TryParse($s, [ref]$v)) { $out += $v } }
  }
  return ($out | Sort-Object)
}

if (-not (Test-Path $In)) { throw "No such file: $In" }
$cut = ConvertTo-Seconds $At
$dur = Probe-Duration $In
if ($cut -le 0 -or $cut -ge $dur) {
  throw ("Split point {0} is outside the file, which runs {1}." -f $At, (Show-Time $dur))
}

$dir  = Split-Path $In -Parent
$base = [IO.Path]::GetFileNameWithoutExtension($In)
if (-not $OutA) { $OutA = Join-Path $dir ($base + '_a.mp4') }
if (-not $OutB) { $OutB = Join-Path $dir ($base + '_b.mp4') }

Write-Host ("using: " + $FFMPEG) -ForegroundColor DarkGray
Write-Host ("{0}  runs {1}, splitting at {2}" -f (Split-Path $In -Leaf), (Show-Time $dur), (Show-Time $cut))

# ---- the second half must start on a keyframe AT OR AFTER the split point,
# never before it, or the tail would repeat the end of the first half.
Write-Host ''
Write-Host 'Locating the first keyframe at or after the split point...' -ForegroundColor DarkGray
$startB = $null
foreach ($window in @(6, 20, 60)) {
  $kf = Get-Keyframes $In ($cut - 0.5) ($cut + $window)
  $cand = $kf | Where-Object { $_ -ge $cut - 0.001 } | Select-Object -First 1
  if ($null -ne $cand) { $startB = [double]$cand; break }
}
if ($null -eq $startB) {
  throw "No keyframe found at or after $At. The file may have very long keyframe intervals."
}

$gap = $startB - $cut
Write-Host ('  first half ends   {0}' -f (Show-Time $cut))
Write-Host ('  second half opens {0}   (keyframe)' -f (Show-Time $startB))
if ($gap -lt 0.25) {
  Write-Host ('  {0:N2}s falls between them - a transition frame, nothing repeated' -f $gap) -ForegroundColor Green
} elseif ($gap -lt 1.0) {
  Write-Host ('  {0:N2}s falls between them - nothing repeated' -f $gap) -ForegroundColor DarkYellow
} else {
  Write-Warning ('{0:N2}s falls between the two halves and will not appear in either. Split at {1} instead if you need that material kept.' -f $gap, (Show-Time $startB))
}

# ---- first half: exact to the frame
Write-Host ''
Write-Host 'Writing the first half...' -ForegroundColor DarkGray
& $FFMPEG -hide_banner -v warning -nostdin -y -i $In -to $cut -c copy -movflags +faststart $OutA
if ($LASTEXITCODE -ne 0) { throw "ffmpeg exited with code $LASTEXITCODE while writing $OutA." }

# ---- second half: from the keyframe to the end
Write-Host 'Writing the second half...' -ForegroundColor DarkGray
& $FFMPEG -hide_banner -v warning -nostdin -y -ss $startB -i $In -c copy -avoid_negative_ts make_zero -movflags +faststart $OutB
if ($LASTEXITCODE -ne 0) { throw "ffmpeg exited with code $LASTEXITCODE while writing $OutB." }

# ---- report
$da = Probe-Duration $OutA
$db = Probe-Duration $OutB
$ma = (Get-Item $OutA).Length / 1MB
$mb = (Get-Item $OutB).Length / 1MB

Write-Host ''
Write-Host ('{0,-30} {1,10}  ({2:N1} MB)' -f (Split-Path $OutA -Leaf), (Show-Time $da), $ma) -ForegroundColor Green
Write-Host ('{0,-30} {1,10}  ({2:N1} MB)' -f (Split-Path $OutB -Leaf), (Show-Time $db), $mb) -ForegroundColor Green

# audio packets do not land exactly on video frames, so allow a little slack
$overlap = ($da + $db) - $dur
if ($overlap -gt 0.5) {
  Write-Warning ('The halves total {0:N2}s more than the original. Check the opening of the second half.' -f $overlap)
} else {
  Write-Host ('together {0} against an original of {1}' -f (Show-Time ($da + $db)), (Show-Time $dur)) -ForegroundColor DarkGray
}
