import os
import re
import json
import yaml
from pathlib import Path

skills_dir = Path(r"C:\Users\Curtis\.gemini\config\skills")
registry_file = skills_dir / "skill_registry.json"

def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    if not file_path.exists():
        return {}
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Match frontmatter (starts with ---, ends with ---)
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            parsed = yaml.safe_load(yaml_content)
            if isinstance(parsed, dict):
                return parsed
    except Exception as e:
        print(f"[Warning] Failed to parse frontmatter for {file_path.name}: {e}")
        
    return {}

def main():
    print("Starting skill registry optimization...")
    registry = {}
    
    if not skills_dir.exists():
        print(f"Skills directory not found at {skills_dir}")
        return
        
    for skill_name in os.listdir(skills_dir):
        skill_path = skills_dir / skill_name
        if skill_path.is_dir():
            skill_file = skill_path / "SKILL.md"
            meta = parse_frontmatter(skill_file)
            
            # Default fallback values
            name = meta.get("name", skill_name)
            description = meta.get("description", f"Skill instructions for {skill_name}")
            triggers = meta.get("activation_triggers", [skill_name.replace("_", " "), skill_name])
            
            registry[skill_name] = {
                "name": name,
                "category": "agent" if skill_name[0].isdigit() else "workflow",
                "description": description,
                "activation_triggers": triggers,
                "tier": meta.get("tier", 0),
                "token_estimate": meta.get("token_estimate", 1000),
                "skill_path": str(skill_file)
            }
            print(f"Registered skill: {name} - {description[:60]}...")
            
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
        
    print(f"Skill registry compiled successfully to {registry_file}")

if __name__ == "__main__":
    main()
