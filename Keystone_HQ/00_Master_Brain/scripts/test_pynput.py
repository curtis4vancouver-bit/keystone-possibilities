import pynput.keyboard as kb
import time

def on_press(key):
    with open("pynput_test.log", "a") as f:
        f.write(f"Pressed {key}\n")

listener = kb.Listener(on_press=on_press)
listener.start()

with open("pynput_test.log", "w") as f:
    f.write("Started\n")

time.sleep(10)
