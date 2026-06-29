import cv2
import os

video_path = r"C:\Users\Curtis\Desktop\short 2.mov"
output_path = r"C:\Users\Curtis\Desktop\short_2_thumbnail.jpg"

if not os.path.exists(video_path):
    print("Video not found.")
    exit(1)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if total_frames == 0 or fps == 0:
    print("Invalid video file.")
    exit(1)

duration = total_frames / fps

# Take a frame from exactly 1 second before the end of the video
target_time = max(0, duration - 1.0)
cap.set(cv2.CAP_PROP_POS_MSEC, target_time * 1000)

ret, frame = cap.read()
if ret:
    cv2.imwrite(output_path, frame)
    print(f"Thumbnail successfully extracted to {output_path}")
else:
    print("Failed to extract frame.")
cap.release()
