import sys
import os
modules_path = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules'
alt_path = r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules'
if os.path.exists(modules_path): sys.path.append(modules_path)
elif os.path.exists(alt_path): sys.path.append(alt_path)

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp('Resolve')
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
media_pool = project.GetMediaPool()

TIMELINE_NAME = "Ana Stevenson — The Gilded Pulse (Full Album)"

# Delete timeline
deleted = False
for i in range(1, project.GetTimelineCount() + 1):
    t = project.GetTimelineByIndex(i)
    if t and t.GetName() == TIMELINE_NAME:
        media_pool.DeleteTimelines([t])
        deleted = True
        break

if deleted:
    print("Timeline wiped successfully.")
else:
    print("No timeline found to wipe.")
