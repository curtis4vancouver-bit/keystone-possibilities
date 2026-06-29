$desktop = [Environment]::GetFolderPath("Desktop")
$root = "$desktop\Keystone_Media_Dropzone"

Write-Host "Creating Dropzone Directories..."
New-Item -ItemType Directory -Path "$root" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\01_Wayne_Reference_Photos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\02_Wayne_General_Photos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\03_New_Raw_Videos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\04_DaVinci_B_Roll_Photos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\05_DaVinci_B_Roll_Videos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\06_AI_Advertising_Assets" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\06_AI_Advertising_Assets\Photos" -Force | Out-Null
New-Item -ItemType Directory -Path "$root\06_AI_Advertising_Assets\Videos" -Force | Out-Null

Write-Host "Setting Custom Folder Icon..."
$iniPath = "$root\desktop.ini"
$iniContent = @"
[.ShellClassInfo]
IconResource=%SystemRoot%\system32\imageres.dll,-114
"@
# Note: imageres.dll, -114 is a media/movie folder icon on Windows 11. 

# Create the desktop.ini file
Set-Content -Path $iniPath -Value $iniContent -Encoding Unicode -Force

# Set desktop.ini to Hidden and System
(Get-Item $iniPath).Attributes = 'Hidden', 'System'

# Set the Root folder to ReadOnly (this is required for Windows to process the desktop.ini)
$rootItem = Get-Item $root
$rootItem.Attributes = $rootItem.Attributes -bor [System.IO.FileAttributes]::ReadOnly

Write-Host "Dropzone successfully created at $root"
