Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*remote-debugging-port*' } | Select-Object Name, CommandLine | Format-List
