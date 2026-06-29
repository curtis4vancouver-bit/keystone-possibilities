from PIL import ImageGrab
import subprocess
import time

subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"])
time.sleep(10)

img = ImageGrab.grab(all_screens=True)
img.save("screenshot_all.png")
print("Screenshot of all monitors saved.")
