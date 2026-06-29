import psutil

print("--- LISTENING PORT ANALYSIS ---")
for conn in psutil.net_connections(kind='inet'):
    if conn.status == 'LISTEN':
        try:
            proc = psutil.Process(conn.pid)
            print(f"PID {conn.pid} ({proc.name()}) is listening on {conn.laddr.ip}:{conn.laddr.port}")
        except Exception:
            print(f"PID {conn.pid} (unknown) is listening on {conn.laddr.ip}:{conn.laddr.port}")
