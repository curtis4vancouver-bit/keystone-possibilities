# deploy_agents.ps1
# This script pins all running headless agent python.exe processes to CPU cores 2-8
# and preserves cores 0-1 for the system, browser, and Multiplexer control surface.

Write-Host "Applying CPU affinity for Python agent processes..."

# Bitmask for Cores 2-8: 
# Core 2 = 4 (2^2)
# Core 3 = 8 (2^3)
# Core 4 = 16 (2^4)
# Core 5 = 32 (2^5)
# Core 6 = 64 (2^6)
# Core 7 = 128 (2^7)
# Core 8 = 256 (2^8)
# Sum = 508 (0x01FC)

$affinityMask = 508

$processes = Get-Process -Name "python" -ErrorAction SilentlyContinue

if ($processes) {
    foreach ($process in $processes) {
        try {
            $process.ProcessorAffinity = [IntPtr]$affinityMask
            Write-Host "Successfully pinned process ID $($process.Id) to cores 2-8."
        }
        catch {
            Write-Warning "Failed to pin process ID $($process.Id): $_"
        }
    }
} else {
    Write-Host "No Python processes found."
}

# Adjust Win32PrioritySeparation for optimal background process scheduling (Server-style, fixed long quantum)
# Value 0x18 (24 decimal) sets fixed, equal, long quantums for foreground and background.
try {
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\PriorityControl" -Name "Win32PrioritySeparation" -Value 24
    Write-Host "Successfully optimized Win32PrioritySeparation for background processes."
} catch {
    Write-Warning "Failed to set Win32PrioritySeparation (requires Administrator privileges)."
}

Write-Host "Deployment agent resource optimization complete."
