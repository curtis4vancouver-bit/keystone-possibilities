import os
import re
from pathlib import Path

MASTER_BRAIN = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
RESEARCH_ARCHIVES = MASTER_BRAIN / "Research_Archives"
CONTENT_PRODUCTION = MASTER_BRAIN / "Content_Production"
DYNAMIC_SKILLS = MASTER_BRAIN / "dynamic_skills"
LIVE_SKILLS = Path(r"C:\Users\Curtis\.gemini\config\skills")

print("--- PHASE 4 AUDIT REPORT ---\n")

# 4a. Research Archives Stubs & Duplicates
print("## 4a. Research Archives")
stubs = []
for f in RESEARCH_ARCHIVES.rglob("*.md"):
    if f.is_file():
        text = f.read_text(encoding="utf-8", errors="ignore")
        if len(text.strip()) < 100 and "_INDEX" not in f.name:
            stubs.append(f.relative_to(MASTER_BRAIN))
print(f"Found {len(stubs)} stub files (<100 chars):")
for s in stubs[:10]:
    print(f"  - {s}")
if len(stubs) > 10:
    print(f"  ... and {len(stubs)-10} more")

# 4c. Content Production Companions
print("\n## 4c. Content Production")
scripts = []
brolls = []
flows = []
for f in CONTENT_PRODUCTION.glob("*.md"):
    if "script" in f.name.lower():
        scripts.append(f.name)
    elif "broll" in f.name.lower() or "b-roll" in f.name.lower():
        brolls.append(f.name)
    elif "flow" in f.name.lower():
        flows.append(f.name)
print(f"Found {len(scripts)} scripts, {len(brolls)} B-roll lists, {len(flows)} Flow segments.")

# 4e. dynamic_skills Match
print("\n## 4e. Dynamic Skills Synchronization")
live_skill_dirs = [d.name for d in LIVE_SKILLS.iterdir() if d.is_dir()]
dynamic_skills = [f.stem for f in DYNAMIC_SKILLS.glob("*.md") if f.name.upper() not in ["_INDEX.MD", "INDEX.MD"]]
outdated = []
for ds in dynamic_skills:
    if ds not in live_skill_dirs:
        # Check if there is a match ignoring numbering prefix
        clean_ds = re.sub(r'^\d+_', '', ds)
        if not any(clean_ds in ls for ls in live_skill_dirs):
            outdated.append(ds)

print(f"Found {len(outdated)} dynamic_skills not matching any live skill folder:")
for ds in outdated:
    print(f"  - {ds}")
