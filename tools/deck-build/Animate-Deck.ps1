<#
  Animate-Deck.ps1 - move the ANIMATIONS instead of the deck.

    .\Animate-Deck.ps1 -Deck "..\ECON003_Ch09_..._v2.pptx" -Export
    (send me the _anim folder; I send it back rewritten)
    .\Animate-Deck.ps1 -Deck "..\ECON003_Ch09_..._v2.pptx" -Apply -Out "..\ECON003_Ch09_..._v3.pptx"

  Why
  ---
  A .pptx is a zip. Once two lecture clips are embedded the Ch09 deck is ~138 MB and
  will not cross the link to me - staging times out. But the animation depends on
  nothing except ppt/slides/*.xml: geometry, shape ids and text, about 1 MB for the
  whole deck. So the video never moves. Only the slide XML does.

  -Export  pulls ppt/slides/slide*.xml into a folder (default: _anim beside the deck).
  -Apply   copies the deck to -Out and swaps those entries back in. Nothing else in
           the package is touched, so the embedded media is bit-for-bit unchanged.

  Slides carrying video keep their own timing and are never rewritten.
#>
param(
  [Parameter(Mandatory=$true)][string]$Deck,
  [switch]$Export,
  [switch]$Apply,
  [string]$Out,
  [string]$Dir
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

if (-not (Test-Path -LiteralPath $Deck)) { throw "No such deck: $Deck" }
$Deck = (Resolve-Path -LiteralPath $Deck).Path
if (-not $Dir) { $Dir = Join-Path (Split-Path -Parent $Deck) '_anim' }

if ($Export) {
  if (-not (Test-Path -LiteralPath $Dir)) { New-Item -ItemType Directory -Path $Dir | Out-Null }
  Get-ChildItem -LiteralPath $Dir -Filter 'slide*.xml' -ErrorAction SilentlyContinue |
    Remove-Item -Force
  $zip = [IO.Compression.ZipFile]::OpenRead($Deck)
  $n = 0
  try {
    foreach ($e in $zip.Entries) {
      if ($e.FullName -match '^ppt/slides/slide\d+\.xml$') {
        $dest = Join-Path $Dir (Split-Path $e.FullName -Leaf)
        [IO.Compression.ZipFileExtensions]::ExtractToFile($e, $dest, $true)
        $n++
      }
    }
  } finally { $zip.Dispose() }
  $mb = (Get-ChildItem -LiteralPath $Dir -Filter 'slide*.xml' |
         Measure-Object Length -Sum).Sum / 1MB
  '{0} slide parts -> {1}  ({2:N2} MB)' -f $n, $Dir, $mb
  Write-Host 'Send that folder over. The deck itself stays here.' -ForegroundColor Cyan
  return
}

if ($Apply) {
  if (-not $Out) { throw "Give me -Out, e.g. -Out '..\ECON003_Ch09_..._v3.pptx'" }
  $files = @(Get-ChildItem -LiteralPath $Dir -Filter 'slide*.xml' -ErrorAction SilentlyContinue)
  if (-not $files) { throw "No slide*.xml in $Dir - run -Export first, and put the rewritten parts there." }

  Copy-Item -LiteralPath $Deck -Destination $Out -Force
  $zip = [IO.Compression.ZipFile]::Open($Out, 'Update')
  $n = 0
  try {
    foreach ($f in $files) {
      $name = 'ppt/slides/' + $f.Name
      $e = $zip.GetEntry($name)
      if (-not $e) { Write-Host "  skip (not in deck): $name" -ForegroundColor Yellow; continue }
      $e.Delete()
      $new = $zip.CreateEntry($name, [IO.Compression.CompressionLevel]::Optimal)
      $s = $new.Open()
      try {
        $bytes = [IO.File]::ReadAllBytes($f.FullName)
        $s.Write($bytes, 0, $bytes.Length)
      } finally { $s.Dispose() }
      $n++
    }
  } finally { $zip.Dispose() }

  $mb = (Get-Item -LiteralPath $Out).Length / 1MB
  '{0}  <-  {1} slide parts replaced  ({2:N1} MB)' -f $Out, $n, $mb
  Write-Host 'Open it and press through a slide to check the clicks.' -ForegroundColor Cyan
  return
}

throw "Pass -Export or -Apply."
