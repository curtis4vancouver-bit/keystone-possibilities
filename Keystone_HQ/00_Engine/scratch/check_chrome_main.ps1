Get-CimInstance Win32_Process -Filter "name = 'chrome.exe' and not CommandLine like '%--type=%'" | Select-Object CommandLine | Format-List
