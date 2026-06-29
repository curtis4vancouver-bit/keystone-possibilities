import os
import time
import pyperclip
import pyautogui
from PIL import ImageGrab
import pygetwindow as gw
import subprocess

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
        let a = document.createElement("a");
        a.href = url;
        a.download = id + ".mp4"; 
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}
downloadVideos();
"""

pyperclip.copy(payload)
subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"])
time.sleep(15)

try:
    for win in gw.getWindowsWithTitle('Flow'):
        win.maximize()
        win.activate()
        time.sleep(1)
        break
except Exception as e:
    print("Window activation failed:", e)

pyautogui.hotkey('ctrl', 'shift', 'j')
time.sleep(3)

img = ImageGrab.grab()
img.save("screenshot_before_paste.png")

pyautogui.hotkey('ctrl', 'v')
time.sleep(1)
pyautogui.press('enter')

time.sleep(1)
img = ImageGrab.grab()
img.save("screenshot_after_paste.png")
