# ================================================
# KEYSTONE APP LAUNCHER
# Double-click to start both servers
# ================================================

$Host.UI.RawUI.WindowTitle = "Keystone App Launcher"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   KEYSTONE APP LAUNCHER                    " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$CONSTRUCTION = "C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites\pwa"

# Check if node/npm is available
$npmPath = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmPath) {
    Write-Host "[ERROR] npm not found! Make sure Node.js is installed." -ForegroundColor Red
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Kill any existing dev servers on 3000
Write-Host "[*] Cleaning up old server processes..." -ForegroundColor Gray
Get-Process -Name node -ErrorAction SilentlyContinue | ForEach-Object {
    $connections = netstat -ano | Select-String ":3000\s" | Select-String $_.Id
    if ($connections) {
        Write-Host "    Stopping old process $($_.Id)..." -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}

Start-Sleep -Seconds 1

# Start Construction PWA (port 3000)
Write-Host ""
Write-Host "[1/1] Starting Keystone Possibilities PWA (port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$CONSTRUCTION'; `$Host.UI.RawUI.WindowTitle = 'Keystone PWA - Port 3000'; npm run dev" -WindowStyle Minimized

Write-Host ""
Write-Host "[OK] PWA server starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "   Construction PWA:    http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Waiting for server to be ready..." -ForegroundColor Gray

# Wait for server to actually be ready
$maxWait = 30
$waited = 0
$pwaReady = $false

while ($waited -lt $maxWait -and (-not $pwaReady)) {
    Start-Sleep -Seconds 2
    $waited += 2
    
    if (-not $pwaReady) {
        try {
            $null = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            $pwaReady = $true
            Write-Host "   [OK] PWA ready!" -ForegroundColor Green
        } catch { }
    }
    
    if (-not $pwaReady) {
        Write-Host "   Waiting... ($waited/$maxWait sec)" -ForegroundColor Gray
    }
}

Write-Host ""

if ($pwaReady) {
    Write-Host "Opening app in browser..." -ForegroundColor Green
    Start-Process "http://localhost:3000"
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "   ALL SYSTEMS GO!                          " -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
} else {
    Write-Host "[WARNING] PWA server may not be ready yet." -ForegroundColor Yellow
    Write-Host "Opening browser anyway - it should load shortly..." -ForegroundColor Yellow
    Start-Process "http://localhost:3000"
}

Write-Host ""
Write-Host "Press any key to exit this launcher (servers keep running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
