# generate_js.py
import json
from pathlib import Path

PENDING_JSON = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\51cde5f0-bd0e-4277-b8fe-c0e5aeda6f75\scratch\pending_downloads.json")
JS_OUTPUT = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\51cde5f0-bd0e-4277-b8fe-c0e5aeda6f75\scratch\download_script.js")

def main():
    if not PENDING_JSON.exists():
        print("[-] pending_downloads.json not found")
        return
        
    with open(PENDING_JSON, "r", encoding="utf-8") as f:
        pending = json.load(f)
        
    # We want to format the list of objects for JS
    js_items = []
    for item in pending:
        js_items.append({
            "id": item["id"],
            "cardIndex": item["cardIndex"],
            "isVideo": item["type"] == "video"
        })
        
    js_code = f"""async () => {{
    const pendingItems = {json.dumps(js_items, indent=2)};
    
    console.log("[+] Starting JS download runner. Total items: " + pendingItems.length);
    
    async function downloadCard(cardIndex, isVideo) {{
        const cards = document.querySelectorAll("[aria-roledescription='draggable']");
        const card = cards[cardIndex];
        if (!card) {{
            console.error("[-] Card not found at index: " + cardIndex);
            return false;
        }}
        const target = card.querySelector("video") || card.querySelector("img") || card.querySelector("a") || card;
        
        card.scrollIntoView({{ block: "center" }});
        await new Promise(r => setTimeout(r, 200));
        
        // Right click
        target.dispatchEvent(new MouseEvent('contextmenu', {{
            bubbles: true, cancelable: true, view: window, buttons: 2
        }}));
        await new Promise(r => setTimeout(r, 450));
        
        // Find Download option
        const menuItems = Array.from(document.querySelectorAll("[role='menuitem']"));
        const downloadItem = menuItems.find(el => el.innerText.includes("Download"));
        if (!downloadItem) {{
            document.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Escape' }}));
            console.error("[-] Download option not found for card: " + cardIndex);
            return false;
        }}
        
        downloadItem.dispatchEvent(new MouseEvent('mouseover', {{ bubbles: true }}));
        downloadItem.click();
        await new Promise(r => setTimeout(r, 450));
        
        // Find resolution
        const submenuItems = Array.from(document.querySelectorAll("[role='menuitem']"));
        let resolutionItem;
        if (isVideo) {{
            resolutionItem = submenuItems.find(el => el.innerText.includes("1080p") || el.innerText.includes("Upscaled") || el.innerText.includes("720p"));
        }} else {{
            resolutionItem = submenuItems.find(el => el.innerText.includes("1K") || el.innerText.includes("Original size"));
        }}
        
        if (!resolutionItem) {{
            document.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Escape' }}));
            console.error("[-] Resolution option not found for card: " + cardIndex);
            return false;
        }}
        
        resolutionItem.click();
        await new Promise(r => setTimeout(r, 200));
        document.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Escape' }}));
        return true;
    }}
    
    // Batch processing
    const BATCH_SIZE = 8;
    for (let i = 0; i < pendingItems.length; i += BATCH_SIZE) {{
        const batch = pendingItems.slice(i, i + BATCH_SIZE);
        console.log("[~] Triggering batch starting at index " + i + " containing: " + batch.map(x => x.id).join(", "));
        
        for (const item of batch) {{
            console.log("  [~] Triggering download for " + item.id + " (Card " + item.cardIndex + ")...");
            await downloadCard(item.cardIndex, item.isVideo);
            // 2 second delay between items to prevent Radix UI menu collisions
            await new Promise(r => setTimeout(r, 2000));
        }}
        
        // Wait 15 seconds for downloads in the batch to complete before next batch
        console.log("[~] Batch triggered. Waiting 15 seconds for downloads to progress...");
        await new Promise(r => setTimeout(r, 15000));
    }}
    
    console.log("[+] All pending downloads triggered successfully in JS!");
    return "All " + pendingItems.length + " downloads triggered!";
}}
"""
    
    with open(JS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(js_code)
        
    print(f"[+] Generated JS download script at {JS_OUTPUT}")

if __name__ == "__main__":
    main()
