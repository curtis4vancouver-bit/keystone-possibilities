Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | Where-Object { $_.CommandLine -notlike '*--type=*' } | Select-Object ProcessId, CommandLine | Format-List
