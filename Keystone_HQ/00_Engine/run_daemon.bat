@echo off
cd /d "c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
python sovereign_coordinator.py --test-all >> Transcripts\background_daemon.log 2>&1
