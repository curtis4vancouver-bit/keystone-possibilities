Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | Select-Object CommandLine | Format-List
