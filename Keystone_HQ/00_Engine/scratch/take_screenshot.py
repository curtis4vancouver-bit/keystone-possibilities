from PIL import ImageGrab
import os

img = ImageGrab.grab()
img.save("screenshot.png")
print("Screenshot saved to screenshot.png")
