<#
  run-this.ps1 - trim parts 5 and 8, then merge W5 1..10 into one chapter.

  Just run  .\run-this.ps1  from the Video folder. Everything below is a lossless
  stream copy - nothing is re-encoded.

  Step 1   W5\5.mp4 -> W5\5_cut.mp4   ending 2:39.4
           (last speech ends 2:38.83; 3.0 s of dead air after it)
  Step 2   W5\8.mp4 -> W5\8_cut.mp4   ending 9:03.5
           (last speech ends 9:02.90; 3.8 s of dead air after it)
  Step 3   merge W5\1..10 -> W5\Chapter 11.mp4   (~95 MB)

  MergeW prefers <n>_cut.mp4 over <n>.mp4, so steps 1 and 2 are picked up
  automatically without renaming anything.
#>

$ErrorActionPreference = 'Stop'
$here = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

Write-Host ''
Write-Host '=== 1/3  trimming part 5 ===' -ForegroundColor Cyan
& (Join-Path $here 'Cut.ps1') (Join-Path $here 'W5\5.mp4') -End 2:39.4 -Out (Join-Path $here 'W5\5_cut.mp4')

Write-Host ''
Write-Host '=== 2/3  trimming part 8 ===' -ForegroundColor Cyan
& (Join-Path $here 'Cut.ps1') (Join-Path $here 'W5\8.mp4') -End 9:03.5 -Out (Join-Path $here 'W5\8_cut.mp4')

Write-Host ''
Write-Host '=== 3/3  merging 1..10 ===' -ForegroundColor Cyan
& (Join-Path $here 'MergeW.ps1') -Folder W5 -Count 10 -Out 'Chapter 11.mp4'
