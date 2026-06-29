def extract_track_name(filename):
    import re
    return re.sub(r'Track \d+_ (.*)\.wav', r'\1', filename)

tracks = [
    ("Track 1_ Kinetic Soul.wav", 131),
    ("Track 2_ Deep Foundation.wav", 181),
    ("Track 3_ The Next Phase.wav", 172),
    ("Track 4_ Velvet Rhythm.wav", 174),
    ("Track 5_ Cello Momentum.wav", 54),
    ("Track 6_ Modern Blueprint.wav", 188),
    ("Track 7_ Steady Drive.wav", 217),
    ("Track 8_ Rhythmic Resilience.wav", 225),
    ("Track 9_ Strength in Focus.wav", 183),
    ("Track 10_ Midnight Pulse.wav", 247),
]

def format_srt_time(seconds):
    hours = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{mins:02d}:{secs:02d},{millis:03d}"

srt_content = ""
current_time = 0.0

for i, (filename, duration) in enumerate(tracks, 1):
    start = format_srt_time(current_time)
    end = format_srt_time(current_time + duration - 0.5) # fade out subtitle 0.5s early
    name = extract_track_name(filename)
    srt_content += f"{i}\n{start} --> {end}\n{name}\n\n"
    current_time += duration

with open('album_subtitles.srt', 'w', encoding='utf-8') as f:
    f.write(srt_content)
print('Created album_subtitles.srt')
