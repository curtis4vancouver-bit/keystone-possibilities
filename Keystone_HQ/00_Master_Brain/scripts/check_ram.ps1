$chromeProc = Get-Process -Name chrome -ErrorAction SilentlyContinue
$chromeCount = if ($chromeProc) { $chromeProc.Count } else { 0 }
$chromeRAM = if ($chromeProc) { [Math]::Round(($chromeProc | Measure-Object WorkingSet -Sum).Sum / 1MB, 2) } else { 0 }

$nodeProc = Get-Process -Name node -ErrorAction SilentlyContinue
$nodeCount = if ($nodeProc) { $nodeProc.Count } else { 0 }
$nodeRAM = if ($nodeProc) { [Math]::Round(($nodeProc | Measure-Object WorkingSet -Sum).Sum / 1MB, 2) } else { 0 }

Write-Output "Chrome Processes: $chromeCount ($chromeRAM MB)"
Write-Output "Node Processes:   $nodeCount ($nodeRAM MB)"
