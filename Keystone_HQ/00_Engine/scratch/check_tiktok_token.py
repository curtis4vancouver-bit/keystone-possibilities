import json
import time

def main():
    try:
        with open('social_tokens.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tiktok = data['recomposition']['tiktok']
        acquired = tiktok['acquired_at']
        expires_in = tiktok['expires_in']
        
        current = time.time()
        elapsed = current - acquired
        remaining = expires_in - elapsed
        
        print(f"TikTok token acquired: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(acquired))}")
        print(f"Elapsed: {elapsed/3600:.2f} hours")
        print(f"Remaining lifespan: {remaining/3600:.2f} hours")
        
        if remaining <= 0:
            print("Token is expired and needs to be refreshed.")
        else:
            print("Token is still valid!")
            
    except Exception as e:
        print(f"Error checking token: {e}")

if __name__ == "__main__":
    main()
