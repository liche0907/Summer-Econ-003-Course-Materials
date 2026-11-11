<#
  Merge.ps1 - join clips end to end without re-encoding.

    .\Merge.ps1 -Out ECON003_Ch03_lecture.mp4 part1_cut.mp4 part2_cut.mp4

  Clips play in the order you list them. They must share codec, resolution,
  frame rate and audio format - true when they come from the same recorder
  with the same settings.
#>
param(
  [Parameter(Mandatory=$true)][string]$Out,
  [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)][string[]]$Parts
)

$ErrorActionPreference = 'Stop'

# Find ffmpeg. Order: next to this script -> any extracted build folder
# below it (e.g. ffmpeg-*-shared\bin) -> whatever is on PATH.
# A "shared" build must be run from its own bin folder so Windows can load
# its DLLs, so we point at it in place rather than copying the exe out.
$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

function Find-Tool([string]$name) {
  $direct = Join-Path $root $name
  if (Test-Path $direct) {
    $dlls = Get-ChildItem -Path $root -Filter '*.dll' -ErrorAction SilentlyContinue
    $nested = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
              ForEach-Object { Get-ChildItem -Path $_.FullName -Recurse -Filter $name -ErrorAction SilentlyContinue } |
              Select-Object -First 1
    # a lone exe with no DLLs beside it, but a full build sitting nearby,
    # means this is a shared build that will not start - use the build instead
    if ($dlls.Count -gt 0 -or -not $nested) { return $direct }
    return $nested.FullName
  }
  $found = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
           ForEach-Object { Get-ChildItem -Path $_.FullName -Recurse -Filter $name -ErrorAction SilentlyContinue } |
           Select-Object -First 1
  if ($found) { return $found.FullName }
  return ($name -replace '\.exe$', '')
}

$FFMPEG  = Find-Tool 'ffmpeg.exe'
$FFPROBE = Find-Tool 'ffprobe.exe'
Write-Host ("using: " + $FFMPEG) -ForegroundColor DarkGray

if ($Parts.Count -lt 2) { throw 'Give me at least two files to join.' }
foreach ($p in $Parts) { if (-not (Test-Path $p)) { throw "No such file: $p" } }

# warn if the clips will not concat cleanly
$sig = @()
foreach ($p in $Parts) {
  $sig += (& $FFPROBE -v error -select_streams v -show_entries stream=codec_name,width,height,r_frame_rate -of csv=p=0 $p) -join ','
}
if (($sig | Select-Object -Unique).Count -gt 1) {
  Write-Warning 'These clips do not share video settings, so a stream copy may fail:'
  for ($i = 0; $i -lt $Parts.Count; $i++) { Write-Warning ('  {0}: {1}' -f $Parts[$i], $sig[$i]) }
}

# concat list: forward slashes only. The demuxer treats \ as an escape char,
# so Windows-style paths make it fail with "No such file or directory".
$list = Join-Path $root 'concat_list.txt'
$Parts |
  ForEach-Object { "file '" + ((Resolve-Path $_).Path -replace '\\', '/') + "'" } |
  Set-Content -Path $list -Encoding ASCII

Write-Host 'Joining:'
Get-Content $list | ForEach-Object { Write-Host "  $_" }

$err = & $FFMPEG -hide_banner -v warning -y -f concat -safe 0 -i $list -c copy -movflags +faststart $Out 2>&1
$code = $LASTEXITCODE
Remove-Item $list -ErrorAction SilentlyContinue

if ($code -ne 0) {
  Write-Host ''
  Write-Host 'ffmpeg said:' -ForegroundColor Yellow
  $err | ForEach-Object { Write-Host "  $_" }
  throw "ffmpeg exited with code $code."
}

$d  = [double](& $FFPROBE -v error -show_entries format=duration -of csv=p=0 $Out)
$mb = (Get-Item $Out).Length / 1MB
'{0}  ->  {1}:{2:00.0}  ({3:N1} MB)' -f $Out, [int][math]::Floor($d / 60), ($d % 60), $mb
