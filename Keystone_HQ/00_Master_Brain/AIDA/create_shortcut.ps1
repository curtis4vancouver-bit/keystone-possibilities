$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

# Remove old AIDA V2 shortcut if it exists
$OldShortcutPath = [System.IO.Path]::Combine($DesktopPath, "AIDA V2.lnk")
if (Test-Path $OldShortcutPath) {
    Remove-Item $OldShortcutPath -Force
}

$ShortcutPath = [System.IO.Path]::Combine($DesktopPath, "AIDA.lnk")
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
}

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA\dist\AIDA_App\AIDA_App.exe"
$Shortcut.WorkingDirectory = "C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA\dist\AIDA_App"
$Shortcut.IconLocation = "C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA\frontend\assets\aida.ico"
$Shortcut.Save()

Write-Host "Created AIDA desktop shortcut successfully."
