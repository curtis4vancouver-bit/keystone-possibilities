import os
import sys

# Import the mvhd duration parser from get_video_duration.py
sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch")
from get_video_duration import get_mov_duration

def main():
    filepath = r"C:\Users\Curtis\Desktop\short 20.mov"
    duration = get_mov_duration(filepath)
    if duration:
        print(f"SUCCESS: Duration = {duration:.2f} seconds")
    else:
        print("FAILED to read duration")

if __name__ == "__main__":
    main()
