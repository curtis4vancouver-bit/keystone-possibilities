import os
import time
import pyperclip
import pyautogui

payload = """
async function downloadVideos() {
    let state = window.__NEXT_DATA__.props.pageProps.trpcState.json.queries;
    let components = [];
    for (let q of state) {
        if (q.queryKey[0] === "project" && q.queryKey[1] === "get") {
            components = q.state.data.components;
            break;
        }
    }
    let uuids = [];
    for (let c of components) {
        if (c.media && c.media.name) uuids.push(c.media.name);
    }
    
    console.log("Found " + uuids.length + " clips. Downloading...");
    
    for (let id of uuids) {
        let url = "https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=" + id + "&mediaUrlType=MEDIA_URL_TYPE_VIDEO_UPSCALED_1080P";
        
        try {
            let resp = await fetch(url);
            let blob = await resp.blob();
            let blobUrl = URL.createObjectURL(blob);
            
            let a = document.createElement("a");
            a.href = blobUrl;
            a.download = id + ".mp4"; 
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            URL.revokeObjectURL(blobUrl);
            console.log("Downloaded", id);
        } catch (e) {
            console.error("Failed", id, e);
        }
    }
    
    let marker = document.createElement("div");
    marker.id = "ANTIGRAVITY_DOWNLOAD_COMPLETE";
    document.body.appendChild(marker);
}
downloadVideos();
"""

print("Killing Chrome...")
os.system("taskkill /F /IM chrome.exe /T")
time.sleep(3)

print("Copying payload to clipboard...")
pyperclip.copy(payload)

import subprocess
print("Launching Chrome...")
subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"])

print("Waiting 15 seconds for page load...")
time.sleep(15)

print("Pressing Ctrl+Shift+J...")
pyautogui.hotkey('ctrl', 'shift', 'j')
time.sleep(3)

print("Pasting payload and pressing enter...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)
pyautogui.press('enter')

print("Payload injected. It will take ~30 seconds for all 24 videos to download.")
