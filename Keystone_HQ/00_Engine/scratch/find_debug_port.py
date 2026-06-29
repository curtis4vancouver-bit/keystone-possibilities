import urllib.request
import json
import socket

def main():
    print("Scanning active listening ports...")
    # Find all listening ports on localhost
    ports_to_check = [9222]
    
    # Also scan ports from 9200 to 9300
    for p in range(9200, 9300):
        if p not in ports_to_check:
            ports_to_check.append(p)
            
    # And check any ports that socket can connect to
    print(f"Checking {len(ports_to_check)} candidate ports...")
    for port in ports_to_check:
        try:
            # First try a quick socket connection to see if port is open
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            result = s.connect_ex(('127.0.0.1', port))
            s.close()
            
            if result == 0:
                print(f"Port {port} is OPEN. Querying /json...")
                # Query /json
                url = f"http://127.0.0.1:{port}/json"
                req = urllib.request.Request(url, headers={'Host': f'127.0.0.1:{port}'})
                with urllib.request.urlopen(req, timeout=1.0) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    print(f"  SUCCESS on Port {port}! Found {len(data)} pages.")
                    for p in data[:3]:
                        print(f"    - {p.get('type')}: {p.get('url')[:80]}")
                    return port
        except Exception as e:
            # print(f"  Error on Port {port}: {e}")
            pass
            
    # If not found, let's do a wider socket search for open TCP ports on localhost
    print("Doing a wider scan for open ports...")
    for port in range(50000, 66000):
        if port == 65047: # skip antigravity port
            continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.02)
            result = s.connect_ex(('127.0.0.1', port))
            s.close()
            if result == 0:
                # Query /json
                url = f"http://127.0.0.1:{port}/json"
                req = urllib.request.Request(url, headers={'Host': f'127.0.0.1:{port}'})
                with urllib.request.urlopen(req, timeout=0.5) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    print(f"  SUCCESS on Port {port}! Found {len(data)} pages.")
                    for p in data[:3]:
                        print(f"    - {p.get('type')}: {p.get('url')[:80]}")
                    return port
        except Exception:
            pass
            
    print("Scan complete. No DevTools port found.")
    return None

if __name__ == "__main__":
    main()
