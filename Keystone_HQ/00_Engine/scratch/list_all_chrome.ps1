Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | Select-Object ProcessId, CommandLine | Format-List
