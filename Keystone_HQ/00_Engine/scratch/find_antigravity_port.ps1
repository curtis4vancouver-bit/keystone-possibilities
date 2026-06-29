$processes = Get-Process -Name Antigravity -ErrorAction SilentlyContinue
if (-not $processes) {
    Write-Output "Antigravity process not found."
    exit
}

$pids = $processes.Id
$connections = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -in $pids }

if ($connections) {
    foreach ($conn in $connections) {
        Write-Output "Found port: $($conn.LocalPort) on process ID: $($conn.OwningProcess)"
    }
} else {
    Write-Output "No listening connections found for Antigravity processes."
}
