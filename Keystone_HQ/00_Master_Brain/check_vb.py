import psutil
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or []).lower()
        if 'voice_bridge.py' in cmd:
            print(f'Running: PID {p.info["pid"]}, {cmd}')
    except Exception as e:
        pass
