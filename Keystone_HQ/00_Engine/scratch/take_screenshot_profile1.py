from PIL import ImageGrab
import subprocess
import time
import os

os.system("taskkill /F /IM chrome.exe /T")
time.sleep(3)

subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--profile-directory=Profile 1", "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"])
time.sleep(15)

img = ImageGrab.grab(all_screens=True)
img.save("screenshot_profile1.png")
print("Screenshot of Profile 1 saved.")
