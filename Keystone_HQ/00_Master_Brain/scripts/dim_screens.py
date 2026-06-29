import ctypes
from ctypes import wintypes
import time
import sys

# Windows API DLLs
user32 = ctypes.WinDLL('user32')
dxva2 = ctypes.WinDLL('dxva2')

# Structures
class PHYSICAL_MONITOR(ctypes.Structure):
    _fields_ = [
        ('hPhysicalMonitor', wintypes.HANDLE),
        ('szPhysicalMonitorDescription', wintypes.WCHAR * 128)
    ]

# Callback signature for EnumDisplayMonitors
MonitorEnumProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMONITOR,
    wintypes.HDC,
    ctypes.POINTER(wintypes.RECT),
    wintypes.LPARAM
)

# Set up argtypes and restypes
user32.EnumDisplayMonitors.argtypes = [wintypes.HDC, ctypes.POINTER(wintypes.RECT), MonitorEnumProc, wintypes.LPARAM]
user32.EnumDisplayMonitors.restype = wintypes.BOOL

dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR.argtypes = [wintypes.HMONITOR, ctypes.POINTER(wintypes.DWORD)]
dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR.restype = wintypes.BOOL

dxva2.GetPhysicalMonitorsFromHMONITOR.argtypes = [wintypes.HMONITOR, wintypes.DWORD, ctypes.POINTER(PHYSICAL_MONITOR)]
dxva2.GetPhysicalMonitorsFromHMONITOR.restype = wintypes.BOOL

dxva2.GetMonitorBrightness.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD)]
dxva2.GetMonitorBrightness.restype = wintypes.BOOL

dxva2.SetMonitorBrightness.argtypes = [wintypes.HANDLE, wintypes.DWORD]
dxva2.SetMonitorBrightness.restype = wintypes.BOOL

dxva2.DestroyPhysicalMonitors.argtypes = [wintypes.DWORD, ctypes.POINTER(PHYSICAL_MONITOR)]
dxva2.DestroyPhysicalMonitors.restype = wintypes.BOOL

def get_brightness_controllers():
    monitors_found = []
    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitors_found.append(hMonitor)
        return True
    
    user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
    
    controllers = []
    
    for hMonitor in monitors_found:
        num_physical = wintypes.DWORD(0)
        if dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hMonitor, ctypes.byref(num_physical)):
            if num_physical.value > 0:
                physical_array = (PHYSICAL_MONITOR * num_physical.value)()
                if dxva2.GetPhysicalMonitorsFromHMONITOR(hMonitor, num_physical.value, physical_array):
                    for idx in range(num_physical.value):
                        h_phys = physical_array[idx].hPhysicalMonitor
                        min_val = wintypes.DWORD(0)
                        cur_val = wintypes.DWORD(0)
                        max_val = wintypes.DWORD(0)
                        if dxva2.GetMonitorBrightness(h_phys, ctypes.byref(min_val), ctypes.byref(cur_val), ctypes.byref(max_val)):
                            controllers.append({
                                'handle': h_phys,
                                'original': cur_val.value,
                                'min': min_val.value,
                                'max': max_val.value,
                                'description': physical_array[idx].szPhysicalMonitorDescription,
                                'array': physical_array,
                                'count': num_physical.value
                            })
    return controllers

def main():
    print("Enumerate monitors and save current brightness levels...")
    controllers = get_brightness_controllers()
    if not controllers:
        print("No monitors with DDC/CI brightness control support found.")
        sys.exit(1)
        
    print(f"Controlling brightness for {len(controllers)} monitor(s):")
    for idx, ctrl in enumerate(controllers):
        print(f"  [{idx}] {ctrl['description']}: Current Brightness = {ctrl['original']}")
        
    # Dim screens to 0 (or minimum supported)
    print("\nDimming screens all the way down to low...")
    for ctrl in controllers:
        low_val = max(5, ctrl['min'])
        print(f"  Setting {ctrl['description']} to {low_val}...")
        dxva2.SetMonitorBrightness(ctrl['handle'], low_val)
        
    print("\nScreens dimmed. Waiting 5 seconds...")
    time.sleep(5)
    
    # Restore screens to original brightness
    print("\nRestoring screens back to original brightness...")
    for ctrl in controllers:
        print(f"  Restoring {ctrl['description']} to {ctrl['original']}...")
        dxva2.SetMonitorBrightness(ctrl['handle'], ctrl['original'])
        
    print("\nFinished!")

if __name__ == '__main__':
    main()
