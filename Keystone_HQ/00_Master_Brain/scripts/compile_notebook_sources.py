import os
import json
import datetime
from pathlib import Path

MASTER_BRAIN = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
COMPILED_DIR = MASTER_BRAIN / "Deep_Research_Results" / "Compiled_Sources"

def compile_file(paths, output_name, title):
    print(f"Compiling {title} to {output_name}...")
    content = [f"# {title}\n*Generated on {datetime.date.today().isoformat()}*\n\n"]
    for path in paths:
        full_path = MASTER_BRAIN / path
        if full_path.exists():
            print(f"  Adding: {path}")
            content.append(f"## File: {path.name}\n\n")
            content.append(full_path.read_text(encoding="utf-8", errors="replace"))
            content.append("\n\n---\n\n")
        else:
            print(f"  Warning: File not found: {path}")
            
    out_path = COMPILED_DIR / output_name
    out_path.write_text("".join(content), encoding="utf-8")
    print(f"  [OK] Saved compiled playbook to {out_path.name}")

def compile_journal():
    print("Compiling Correction Journal to Correction_Journal_Playbook.md...")
    journal_path = MASTER_BRAIN / ".learnings" / "correction_journal.json"
    if not journal_path.exists():
        print(f"  Warning: Correction Journal not found: {journal_path}")
        return
        
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except Exception as e:
        print(f"  Error reading journal: {e}")
        return
        
    content = [f"# Keystone Correction Journal & Prevention Playbook\n*Compiled on {datetime.date.today().isoformat()} - Total entries: {len(entries)}*\n\n"]
    for idx, entry in enumerate(entries, 1):
        timestamp = entry.get("timestamp", "N/A")
        error = entry.get("error", "N/A")
        fix = entry.get("fix", "N/A")
        prevention = entry.get("prevention", "N/A")
        scope = entry.get("scope", "general")
        
        content.append(f"## Entry {idx}: [{scope}] - {timestamp}\n")
        content.append(f"### 🛑 Error / Bug:\n{error}\n\n")
        content.append(f"### 🛠️ Fix Applied:\n{fix}\n\n")
        content.append(f"### 🛡️ Prevention Rule:\n{prevention}\n\n")
        content.append("---\n\n")
        
    out_path = COMPILED_DIR / "Correction_Journal_Playbook.md"
    out_path.write_text("".join(content), encoding="utf-8")
    print(f"  [OK] Saved journal playbook to {out_path.name}")

def main():
    os.makedirs(COMPILED_DIR, exist_ok=True)
    
    # 1. Tech Master Playbook
    compile_file(
        paths=[
            Path("AGENTS.md"),
            Path("GEO_AEO_IMPLEMENTATION_PLAYBOOK.md"),
            Path("DEEP_RESEARCH_PROMPTS_SYSTEM_LOCKDOWN.md"),
            Path("INDEX.md")
        ],
        output_name="Tech_Master_Playbook.md",
        title="Keystone Tech Master Playbook"
    )
    
    # 2. Brand Sovereign Bible
    compile_file(
        paths=[
            Path("Brand_Constitution/BRAND_VOICE.md"),
            Path("Brand_Constitution/BRAND_VISUAL.md"),
            Path("Brand_Constitution/CURRENT_DIRECTION.md"),
            Path("DIRECTIVES.md")
        ],
        output_name="Brand_Sovereign_Bible.md",
        title="Keystone Brand Sovereign Bible"
    )
    
    # 3. Journal Playbook
    compile_journal()

if __name__ == "__main__":
    main()
