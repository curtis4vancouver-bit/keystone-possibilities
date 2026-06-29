import sys
import os

sys.path.append(r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules')
import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp('Resolve')
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
mediaPool = project.GetMediaPool()

fps = project.GetSetting('timelineFrameRate')
print('Project FPS:', fps)
