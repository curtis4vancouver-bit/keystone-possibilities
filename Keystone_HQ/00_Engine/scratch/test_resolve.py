import sys
import os

modules_path = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules'
alt_path = r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules'

if os.path.exists(modules_path):
    sys.path.append(modules_path)
elif os.path.exists(alt_path):
    sys.path.append(alt_path)

import DaVinciResolveScript as dvr

resolve = dvr.scriptapp('Resolve')
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
timeline = project.GetCurrentTimeline()
print([func for func in dir(timeline) if 'Title' in func or 'Text' in func or 'Insert' in func])
