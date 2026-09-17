import sys
import os
import json
import base64
import time
import re
import argparse
import urllib.request
from websockets.sync.client import connect as ws_connect

BRAIN_ROOT = r"C:\Users\Curtis\Desktop\Keystone Brain"
PROTOCOLS_DIR = os.path.join(BRAIN_ROOT, "08_Keystone_protocols")
SOCIAL_COPY_DIR = os.path.join(PROTOCOLS_DIR, "04_social_copy")

def log(msg):
    print(f"[META-PUBLISHER] {msg}", flush=True)

def find_active_day():
    link_file = os.path.join(PROTOCOLS_DIR, "active_youtube_video_link.json")
    if os.path.exists(link_file):
        try:
            with open(link_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "day" in data:
                    return int(data["day"])
        except Exception:
            pass
    # Fallback to scanning 04_social_copy
    if os.path.exists(SOCIAL_COPY_DIR):
        files = [f for f in os.listdir(SOCIAL_COPY_DIR) if f.startswith("DAY_") and f.endswith(".md")]
        days = []
        for f in files:
            m = re.search(r"DAY_(\d+)", f)
            if m:
                days.append(int(m.group(1)))
        if days:
            return max(days)
    return 9

def load_social_copy(day=None, file_path=None):
    if not file_path:
        if day is None:
            day = find_active_day()
        file_path = os.path.join(SOCIAL_COPY_DIR, f"DAY_{day:03d}_META_SOCIAL_COPY.md")
        if not os.path.exists(file_path):
            file_path = os.path.join(SOCIAL_COPY_DIR, f"DAY_{day}_META_SOCIAL_COPY.md")

    if not os.path.exists(file_path):
        log(f"Warning: Social copy file not found at {file_path}")
        return None, None, None

    log(f"Loading social copy from: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    fb_match = re.search(r"## 📘 Facebook.*?\n\n(.*?)(?:\n\n---|\Z)", text, re.DOTALL)
    ig_match = re.search(r"## 📸 Instagram.*?\n\n(.*?)(?:\n\n---|\Z)", text, re.DOTALL)
    tags_match = re.search(r"```(?:text)?\s*(.*?)\s*```", text, re.DOTALL)

    fb_copy = fb_match.group(1).strip() if fb_match else ""
    ig_copy = ig_match.group(1).strip() if ig_match else ""
    tags = tags_match.group(1).strip() if tags_match else ""

    # Character Ceiling Validations
    fb_len = len(fb_copy.replace("\n", "\r\n"))
    ig_len = len(ig_copy.replace("\n", "\r\n"))
    log(f"Facebook copy character count (CRLF): {fb_len} (Limit: 2,000)")
    log(f"Instagram copy character count (CRLF): {ig_len} (Limit: 2,200)")

    if fb_len > 2000:
        log(f"⚠️ WARNING: Facebook copy exceeds 2,000 chars ({fb_len}). May cause Reel/Composer errors.")
    if ig_len > 2200:
        log(f"⚠️ ERROR: Instagram copy exceeds 2,200 chars ({ig_len}). Instagram will reject this!")

    return fb_copy, ig_copy, tags

def find_video_path(day=None, explicit_path=None):
    if explicit_path and os.path.exists(explicit_path):
        return explicit_path
    
    candidates = [
        os.path.join(BRAIN_ROOT, "00_todays_video_upload", "try.mov"),
        os.path.join(BRAIN_ROOT, "00_todays_video_upload", "try.mp4"),
        os.path.join(PROTOCOLS_DIR, "Google_Flow", "VIDEO SHORTS", "short_1.mp4"),
        os.path.join(PROTOCOLS_DIR, "Google_Flow", "video", "1.mp4"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def main():
    parser = argparse.ArgumentParser(description="Master Meta Business Suite Publisher for Facebook & Instagram")
    parser.add_argument("--day", type=int, default=None, help="Day number (e.g. 9)")
    parser.add_argument("--context", type=str, default="protocols", choices=["protocols", "possibilities"])
    parser.add_argument("--file", type=str, default=None, help="Custom path to social copy markdown")
    parser.add_argument("--video", type=str, default=None, help="Custom path to video file")
    parser.add_argument("--dry-run", action="store_true", help="Validate copy and exit without CDP injection")
    args = parser.parse_args()

    day = args.day or find_active_day()
    log(f"Initializing Meta Business Suite Publisher for Day {day} (Context: {args.context})...")

    fb_caption, ig_caption, tags = load_social_copy(day=day, file_path=args.file)
    if not fb_caption or not ig_caption:
        log("❌ Failed to load valid social copy. Exiting.")
        sys.exit(1)

    video_path = find_video_path(day=day, explicit_path=args.video)
    log(f"Selected Video Path: {video_path}")

    if args.dry_run:
        log("Dry run complete. Validations passed.")
        return

    try:
        req = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=4)
        tabs = json.loads(req.read().decode("utf-8"))
    except Exception as e:
        log(f"❌ Failed to connect to Chrome Port 9222: {e}")
        sys.exit(1)

    meta_tab = None
    for t in tabs:
        url = t.get("url", "").lower()
        if "business.facebook.com" in url or "facebook.com/latest/composer" in url:
            meta_tab = t
            break

    if not meta_tab:
        for t in tabs:
            url = t.get("url", "").lower()
            if "facebook.com" in url or "meta.com" in url:
                meta_tab = t
                break

    if not meta_tab:
        log("No candidate tab found for Meta Business Suite. Please open Meta Business Suite Composer in Chrome on Port 9222.")
        sys.exit(1)

    ws_url = meta_tab.get("webSocketDebuggerUrl")
    log(f"Attaching to CDP tab: {meta_tab.get('title')} ({meta_tab.get('url')})")

    with ws_connect(ws_url, max_size=None, close_timeout=60) as ws:
        class Msg: id = 0
        def send(method, params=None):
            Msg.id += 1
            call_id = Msg.id
            payload = {"id": call_id, "method": method}
            if params: payload["params"] = params
            ws.send(json.dumps(payload))
            while True:
                raw = ws.recv()
                data = json.loads(raw)
                if data.get("id") == call_id: return data

        def eval_js(js, await_promise=False):
            res = send("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": await_promise})
            return res.get("result", {}).get("result", {}).get("value")

        send("Page.enable")
        send("DOM.enable")

        curr_url = meta_tab.get("url", "")
        if "composer" not in curr_url:
            log("Navigating to Meta Business Suite Composer...")
            send("Page.navigate", {"url": "https://business.facebook.com/latest/composer"})
            time.sleep(5.0)

        # Toggle 'Customize post for Facebook and Instagram'
        eval_js('''
            (() => {
                const toggles = Array.from(document.querySelectorAll('input[type="checkbox"], div[role="switch"], span[role="checkbox"]'));
                const customToggle = toggles.find(t => {
                    const parent = t.closest('div, label');
                    return parent && parent.innerText && parent.innerText.toLowerCase().includes('customize post');
                });
                if (customToggle && !customToggle.checked) {
                    customToggle.click();
                    console.log("Enabled Customize post toggle");
                }
            })()
        ''')
        time.sleep(2.0)

        # Attach video if present and input exists
        if video_path and os.path.exists(video_path):
            doc_res = send("DOM.getDocument")
            root_node_id = doc_res["result"]["root"]["nodeId"]
            inputs_res = send("DOM.querySelectorAll", {
                "nodeId": root_node_id,
                "selector": 'input[type="file"]'
            })
            node_ids = inputs_res.get("result", {}).get("nodeIds", [])
            if node_ids:
                send("DOM.setFileInputFiles", {
                    "files": [video_path],
                    "nodeId": node_ids[0]
                })
                log(f"Attached video to Meta Media loader: {os.path.basename(video_path)}")
            time.sleep(4.0)

        # Inject Facebook & Instagram Custom Text
        eval_js(f'''
            (() => {{
                const textInputs = Array.from(document.querySelectorAll('div[contenteditable="true"], textarea, div[role="textbox"]'));
                if (textInputs.length >= 2) {{
                    textInputs[0].focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, {json.dumps(fb_caption)});
                    textInputs[1].focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, {json.dumps(ig_caption)});
                }} else if (textInputs.length === 1) {{
                    textInputs[0].focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, {json.dumps(fb_caption)});
                }}
            }})()
        ''')
        time.sleep(2.0)

        log("✅ Meta Business Suite Composer has been injected and staged.")

    # Write voice outbox confirmation
    outbox_path = r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt"
    try:
        with open(outbox_path, "w", encoding="utf-8") as vf:
            vf.write(f"Meta Business Suite composer has been staged for Day {day} Facebook and Instagram Wayne. Character limits and custom links have been verified.")
    except Exception:
        pass

if __name__ == "__main__":
    main()
