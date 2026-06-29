@echo off
:loop
echo Starting Voice Bridge...
python -u "c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\voice_bridge.py"
echo Voice Bridge crashed. Restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto loop
