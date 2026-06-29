# run_sync.ps1 - PowerShell runner for Keystone Brand Brain watchdog synchronization daemon
$DaemonScript = "sync_daemon.py"
$LogFile = "scratch\sync_daemon.log"

# Get absolute path
$ScriptPath = Join-Path (Get-Location) $DaemonScript
$LogPath = Join-Path (Get-Location) $LogFile

Write-Host "Checking if sync daemon is already running..." -ForegroundColor Cyan

# Check if there is an existing python process running sync_daemon.py
$ExistingProcess = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' and CommandLine like '%sync_daemon.py%'"

if ($ExistingProcess) {
    Write-Host "WARNING: Sync daemon is already running under Process ID: $($ExistingProcess.ProcessId)" -ForegroundColor Yellow
    Write-Host "You can stop it with: Stop-Process -Id $($ExistingProcess.ProcessId)" -ForegroundColor Yellow
    Exit
}

Write-Host "Starting Keystone watchdog sync daemon in the background..." -ForegroundColor Green
$Process = Start-Process python -ArgumentList "sync_daemon.py" -NoNewWindow -PassThru -WorkingDirectory (Get-Location)

if ($Process) {
    Write-Host "SUCCESS: Started watchdog sync daemon successfully!" -ForegroundColor Green
    Write-Host "Process ID: $($Process.Id)" -ForegroundColor Green
    Write-Host "Sync Log Path: $LogPath" -ForegroundColor Green
    Write-Host "To monitor logs in real-time, run: Get-Content -Path '$LogPath' -Wait" -ForegroundColor Cyan
} else {
    Write-Host "ERROR: Failed to start sync daemon." -ForegroundColor Red
}
