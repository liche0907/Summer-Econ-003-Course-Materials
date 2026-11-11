<#
  Get-Clip.ps1 - pull a streamed clip (HLS / .m3u8) down to a real MP4.

    .\Get-Clip.ps1 https://criticalcommons.org/media/hls/<id>/master.m3u8 -Out "Clips\[Commons]Friends Candy.mp4"
    .\Get-Clip.ps1 <url> -List                        show the renditions, download nothing
    .\Get-Clip.ps1 <url> -Out "Clips\x.mp4" -Rendition 2

  Why this is needed
  ------------------
  An .m3u8 is a PLAYLIST, not a video: a few lines of text pointing at
  hundreds of small .ts segments. Right-click-save gets you the text file,
  which is why the clip looks impossible to download. ffmpeg walks the
  playlist and stitches the segments back into one file.

  Nothing is re-encoded, so this takes seconds and the video and audio are
  bit-for-bit the stream's own - same principle as Cut.ps1 and Merge.ps1.

  Then trim it the usual way:
      .\Cut.ps1 "Clips\[Commons]Friends Candy.mp4" -Start 0:12 -End 1:47

  Naming: the Clips folder uses [Topic]Title.mp4, and the deck links these
  as RELATIVE paths, so renaming a file later means re-pointing the link in
  PowerPoint. Pick the name now.
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$Url,
  [string]$Out,
  [int]$Rendition = -1,
  [switch]$List
)

$ErrorActionPreference = 'Stop'

# Find ffmpeg. Same resolution order as Cut.ps1: next to this script -> any
# extracted build folder below it (e.g. ffmpeg-*-shared\bin) -> PATH.
# A "shared" build must run from its own bin folder so Windows can load its
# DLLs, so we point at it in place rather than copying the exe out.
$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

function Find-Tool([string]$name) {
  $direct = Join-Path $root $name
  if (Test-Path $direct) {
    $dlls = Get-ChildItem -Path $root -Filter '*.dll' -ErrorAction SilentlyContinue
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
  return ($name -replace '\.exe$', '')
}

$FFMPEG  = Find-Tool 'ffmpeg.exe'
$FFPROBE = Find-Tool 'ffprobe.exe'
Write-Host ("using: " + $FFMPEG) -ForegroundColor DarkGray

# Most CDNs refuse a request that does not look like it came from a browser.
# Header lines must be CRLF-terminated, hence the "`r`n".
$hdr = "Referer: https://criticalcommons.org/`r`nOrigin: https://criticalcommons.org`r`n"
$ua  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

# Shared connection options. rw_timeout stops a dropped segment server from
# hanging the download forever; the reconnect flags ride out a blip.
$net = @(
  '-headers', $hdr,
  '-user_agent', $ua,
  '-rw_timeout', '15000000',
  '-reconnect', '1',
  '-reconnect_streamed', '1',
  '-reconnect_delay_max', '5'
)

if ($List) {
  Write-Host "`nrenditions in this playlist:" -ForegroundColor Cyan
  & $FFPROBE -hide_banner @net -i $Url 2>&1 |
    Select-String -Pattern 'Program|Stream #' |
    ForEach-Object { Write-Host ("  " + $_.Line.Trim()) }
  Write-Host "`npass -Rendition N to pin one (N is the Program number).`n"
  return
}

if (-not $Out) { throw "Give me -Out, e.g. -Out `"Clips\[Topic]Name.mp4`"" }

$dir = Split-Path -Parent $Out
if ($dir -and -not (Test-Path -LiteralPath $dir)) {
  New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# -c copy remuxes rather than re-encodes. aac_adtstoasc strips the ADTS
# framing HLS audio carries, which MP4 will not accept - leave it out and the
# audio comes through silent or refuses to mux at all.
$args = @('-hide_banner', '-v', 'warning', '-y') + $net + @('-i', $Url)
if ($Rendition -ge 0) { $args += @('-map', "0:p:$Rendition") }
$args += @('-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-movflags', '+faststart', $Out)

Write-Host "downloading..." -ForegroundColor DarkGray
$err = & $FFMPEG @args 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Host 'ffmpeg said:' -ForegroundColor Yellow
  $err | ForEach-Object { Write-Host "  $_" }
  Write-Host ''
  Write-Host 'If that was a 403 or 404, the stream may need a session cookie:' -ForegroundColor Yellow
  Write-Host '  open the item page in Chrome, DevTools > Network, reload, right-click' -ForegroundColor Yellow
  Write-Host '  the .m3u8 request > Copy as cURL, and read the Cookie header off it.' -ForegroundColor Yellow
  throw "ffmpeg exited with code $LASTEXITCODE."
}

$d  = [double](& $FFPROBE -v error -show_entries format=duration -of csv=p=0 -- $Out)
$mb = (Get-Item -LiteralPath $Out).Length / 1MB
'{0}  ->  {1}:{2:00.0}  ({3:N1} MB)' -f $Out, [int][math]::Floor($d / 60), ($d % 60), $mb

if ($mb -gt 25) {
  Write-Host ''
  Write-Host ("NOTE: {0:N0} MB. Link this from the deck, do not embed it -" -f $mb) -ForegroundColor Yellow
  Write-Host '      an embedded clip carries its own timing data and bloats the file.' -ForegroundColor Yellow
  Write-Host '      Trim it with Cut.ps1 first; clips only need the 60-90 seconds you play.' -ForegroundColor Yellow
}
