import struct
import sys
import os

def get_mov_duration(filepath):
    """Parses a MOV/MP4 file's mvhd atom to extract the duration in seconds."""
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, 'rb') as f:
        # Search for 'mvhd' atom
        file_size = os.path.getsize(filepath)
        chunk = f.read(1024 * 1024)  # Read first MB, usually mvhd is near the beginning
        
        idx = chunk.find(b'mvhd')
        if idx == -1:
            # Try searching the whole file if not in the first MB
            f.seek(0)
            data = f.read()
            idx = data.find(b'mvhd')
            if idx == -1:
                return None
            chunk = data
            
        # The mvhd atom format:
        # 4 bytes size, 4 bytes 'mvhd', 1 byte version, 3 bytes flags
        # Then either (version 0):
        #   4 bytes creation time, 4 bytes modification time, 4 bytes timescale, 4 bytes duration
        # Or (version 1):
        #   8 bytes creation time, 8 bytes modification time, 4 bytes timescale, 8 bytes duration
        
        mvhd_pos = idx
        # Let's seek to version byte which is at mvhd_pos + 4
        version = chunk[mvhd_pos + 4]
        
        if version == 0:
            timescale_pos = mvhd_pos + 4 + 4 + 4 + 4 # skip version/flags (4), creation (4), mod (4)
            timescale = struct.unpack('>I', chunk[timescale_pos:timescale_pos+4])[0]
            duration = struct.unpack('>I', chunk[timescale_pos+4:timescale_pos+8])[0]
        elif version == 1:
            timescale_pos = mvhd_pos + 4 + 4 + 8 + 8 # skip version/flags (4), creation (8), mod (8)
            timescale = struct.unpack('>I', chunk[timescale_pos:timescale_pos+4])[0]
            duration = struct.unpack('>Q', chunk[timescale_pos+4:timescale_pos+12])[0]
        else:
            return None
            
        if timescale > 0:
            return duration / timescale
    return None

def main():
    filepath = r"C:\Users\Curtis\Desktop\short 21.mov"
    duration = get_mov_duration(filepath)
    if duration:
        print(f"SUCCESS: Duration = {duration:.2f} seconds")
    else:
        print("FAILED to read duration")

if __name__ == "__main__":
    main()
