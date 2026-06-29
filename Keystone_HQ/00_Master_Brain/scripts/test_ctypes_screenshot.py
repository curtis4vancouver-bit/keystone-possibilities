import ctypes
from PIL import Image

# Windows API constants
SRCCOPY = 0x00CC0020

def capture_screen_ctypes():
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    
    # 1. Get screen dimensions
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    print(f"[ctypes] Resolution: {width}x{height}")
    
    # 2. Get DC handles
    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    
    # 3. Create compatible bitmap
    hbmp = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
    
    # 4. Select bitmap into memory DC
    old_bmp = gdi32.SelectObject(hdc_mem, hbmp)
    
    # 5. Perform BitBlt transfer
    success = gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_screen, 0, 0, SRCCOPY)
    
    if not success:
        print("[ctypes] Error: BitBlt failed!")
        # Clean up
        gdi32.SelectObject(hdc_mem, old_bmp)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteDC(hdc_mem)
        user32.ReleaseDC(0, hdc_screen)
        return False
        
    # 6. Allocate memory for bitmap pixels
    bmp_info = bytearray(40) # BITMAPINFOHEADER is 40 bytes
    ctypes.struct_pack_into(
        '=IiiHHIIiiII', bmp_info, 0,
        40, width, -height, 1, 32, 0, width * height * 4, 0, 0, 0, 0
    )
    
    # Alternatively, use ctypes structure
    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', ctypes.c_uint32),
            ('biWidth', ctypes.c_int32),
            ('biHeight', ctypes.c_int32),
            ('biPlanes', ctypes.c_int16),
            ('biBitCount', ctypes.c_int16),
            ('biCompression', ctypes.c_uint32),
            ('biSizeImage', ctypes.c_uint32),
            ('biXPelsPerMeter', ctypes.c_int32),
            ('biYPelsPerMeter', ctypes.c_int32),
            ('biClrUsed', ctypes.c_uint32),
            ('biClrImportant', ctypes.c_uint32)
        ]
        
    header = BITMAPINFOHEADER(
        biSize=40, biWidth=width, biHeight=-height, biPlanes=1, biBitCount=32,
        biCompression=0, biSizeImage=width*height*4, biXPelsPerMeter=0, biYPelsPerMeter=0,
        biClrUsed=0, biClrImportant=0
    )
    
    buffer = ctypes.create_string_buffer(width * height * 4)
    
    # Retrieve bitmap bits
    copied_lines = gdi32.GetDIBits(
        hdc_screen, hbmp, 0, height, buffer, ctypes.byref(header), 0
    )
    
    print(f"[ctypes] Copied {copied_lines} lines of bitmap data.")
    
    # Clean up handles
    gdi32.SelectObject(hdc_mem, old_bmp)
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)
    
    if copied_lines > 0:
        # Convert BGRA buffer to RGBA Image
        img = Image.frombuffer("RGBA", (width, height), buffer.raw, "raw", "BGRA", 0, 1)
        img.convert("RGB").save("ctypes_screenshot.png")
        print("[ctypes] Saved ctypes_screenshot.png successfully!")
        return True
    else:
        print("[ctypes] Error: GetDIBits returned 0 copied lines.")
        return False

if __name__ == "__main__":
    capture_screen_ctypes()
