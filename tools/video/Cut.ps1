<#
  Cut.ps1 - trim a recording without re-encoding.

    .\Cut.ps1 lecture.mp4 -End 17:11
    .\Cut.ps1 lecture.mp4 -End 17:11 -Start 0:03
    .\Cut.ps1 lecture.mp4 -End 1031            (plain seconds work too)

  Times accept  SS  |  MM:SS  |  HH:MM:SS.
  Output is <name>_cut.mp4 unless you pass -Out.
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$In,
  [Parameter(Mandatory=$true)][string]$End,
  [string]$Start = '0',
  [string]$Out
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

function ConvertTo-Seconds([string]$t) {
  $p = $t.Split(':')
  switch ($p.Count) {
    1 { [double]$p[0] }
    2 { [double]$p[0] * 60 + [double]$p[1] }
    3 { [double]$p[0] * 3600 + [double]$p[1] * 60 + [double]$p[2] }
    default { throw "Cannot read the time '$t'. Use SS, MM:SS or HH:MM:SS." }
  }
}

if (-not (Test-Path $In)) { throw "No such file: $In" }
$s = ConvertTo-Seconds $Start
$e = ConvertTo-Seconds $End
if ($e -le $s) { throw "End ($End) must be later than Start ($Start)." }
if (-not $Out) { $Out = [IO.Path]::GetFileNameWithoutExtension($In) + '_cut.mp4' }

if ($s -eq 0) {
  $err = & $FFMPEG -hide_banner -v warning -y -i $In -to $e -c copy -movflags +faststart $Out 2>&1
} else {
  $dur = $e - $s
  $err = & $FFMPEG -hide_banner -v warning -y -ss $s -i $In -t $dur -c copy -movflags +faststart $Out 2>&1
}
if ($LASTEXITCODE -ne 0) {
  Write-Host 'ffmpeg said:' -ForegroundColor Yellow
  $err | ForEach-Object { Write-Host "  $_" }
  throw "ffmpeg exited with code $LASTEXITCODE."
}

$d  = [double](& $FFPROBE -v error -show_entries format=duration -of csv=p=0 $Out)
$mb = (Get-Item $Out).Length / 1MB
'{0}  ->  {1}:{2:00.0}  ({3:N1} MB)' -f $Out, [int][math]::Floor($d / 60), ($d % 60), $mb
