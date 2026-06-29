$aidaProc = Get-Process | Where-Object { $_.Name -like "*AIDA*" }
if ($aidaProc) {
    foreach ($p in $aidaProc) {
        Write-Output "AIDA Process: $($p.Name) (PID: $($p.Id))"
    }
} else {
    Write-Output "No processes matching AIDA found."
}
