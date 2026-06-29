import os
import re
import yaml
import tempfile
import time
import json
from typing import Dict, Any, List, Optional

class SkillGenerator:
    """
    Validates, writes, and curates autonomous agent skills.
    Maintains a metadata registry tracking skill usage metrics and handles automatic
    archiving of stale skills.
    """
    SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
        self.auto_gen_dir = os.path.join(skills_dir, "auto-generated")
        self.archive_dir = os.path.join(self.auto_gen_dir, "archive")
        self.usage_file = os.path.join(self.auto_gen_dir, ".usage.json")
        
        os.makedirs(self.auto_gen_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        self.usage_data = self._load_usage()

    def _load_usage(self) -> Dict[str, Any]:
        """Loads usage logs or initializes if not present."""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_usage(self):
        """Saves usage ledger atomically."""
        temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(self.usage_file), suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(self.usage_data, f, indent=4)
            os.replace(temp_path, self.usage_file)
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e

    def validate_skill(self, content: str) -> Tuple[bool, str]:
        """
        Validates the proposed skill against strict constraints:
        - Frontmatter exists and is parseable YAML
        - name <= 64 characters, matches regex
        - description <= 1024 characters
        - total size <= 100KB
        """
        if len(content) > 100 * 1024:
            return False, "Skill content exceeds 100KB limit."

        # Parse YAML frontmatter
        if not content.startswith("---"):
            return False, "Skill must start with YAML frontmatter delimiter '---'."
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            return False, "Malformed YAML frontmatter. Closing '---' delimiter missing."
        
        raw_yaml = parts[1]
        try:
            frontmatter = yaml.safe_load(raw_yaml)
        except Exception as e:
            return False, f"Failed to parse frontmatter YAML: {e}"

        if not isinstance(frontmatter, dict):
            return False, "YAML frontmatter must parse as a dictionary."

        # Check required fields
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        
        if not name:
            return False, "Field 'name' is required in frontmatter."
        if not description:
            return False, "Field 'description' is required in frontmatter."

        if len(name) > 64:
            return False, f"Skill name '{name}' exceeds 64 characters."
        if len(description) > 1024:
            return False, "Description exceeds 1024 characters."

        if not self.SKILL_NAME_PATTERN.match(name):
            return False, f"Skill name '{name}' is invalid. Must be lowercase, start with a letter/number, and contain only a-z, 0-9, dot, underscore, or hyphen."

        return True, ""

    def write_skill(self, content: str) -> str:
        """
        Validates and writes skill atomically using a temporary file.
        Updates usage registry.
        """
        is_valid, err = self.validate_skill(content)
        if not is_valid:
            raise ValueError(f"Skill validation failed: {err}")

        # Extract name from frontmatter
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        name = frontmatter["name"]

        skill_folder = os.path.join(self.auto_gen_dir, name)
        os.makedirs(skill_folder, exist_ok=True)
        
        skill_file = os.path.join(skill_folder, "SKILL.md")
        
        # Atomic write
        temp_fd, temp_path = tempfile.mkstemp(dir=skill_folder, suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(temp_path, skill_file)
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e

        # Initialize usage logs
        if name not in self.usage_data:
            self.usage_data[name] = {
                "use_count": 0,
                "view_count": 0,
                "patch_count": 0,
                "last_activity_at": time.time(),
                "state": "active",
                "pinned": False
            }
        else:
            self.usage_data[name]["patch_count"] += 1
            self.usage_data[name]["last_activity_at"] = time.time()
            self.usage_data[name]["state"] = "active"
            
        self._save_usage()
        return skill_file

    def track_use(self, name: str, is_view: bool = False):
        """Logs usage/views in the registry."""
        if name in self.usage_data:
            if is_view:
                self.usage_data[name]["view_count"] += 1
            else:
                self.usage_data[name]["use_count"] += 1
            self.usage_data[name]["last_activity_at"] = time.time()
            self._save_usage()

    def pin_skill(self, name: str, pinned: bool = True):
        """Pins a skill to protect it from automatic curation."""
        if name in self.usage_data:
            self.usage_data[name]["pinned"] = pinned
            self._save_usage()

    def curate_stale_skills(self, idle_days: int = 30) -> int:
        """
        Scans auto-generated skills and moves those idle for > idle_days to the archive directory.
        Pinned skills are excluded from archiving.
        """
        now = time.time()
        idle_threshold_seconds = idle_days * 86400
        archived_count = 0

        for name, metrics in list(self.usage_data.items()):
            if metrics.get("pinned"):
                continue
            
            last_active = metrics.get("last_activity_at", 0)
            if (now - last_active) > idle_threshold_seconds and metrics.get("state") == "active":
                skill_folder = os.path.join(self.auto_gen_dir, name)
                if os.path.exists(skill_folder):
                    dest_folder = os.path.join(self.archive_dir, name)
                    try:
                        # Move folder to archive
                        if os.path.exists(dest_folder):
                            # Clean up old archive folder if exists
                            import shutil
                            shutil.rmtree(dest_folder)
                        os.rename(skill_folder, dest_folder)
                        
                        # Update state
                        self.usage_data[name]["state"] = "archived"
                        self.usage_data[name]["last_activity_at"] = now
                        archived_count += 1
                        print(f"[SkillGenerator] Archived stale skill '{name}' (idle > {idle_days} days).")
                    except Exception as e:
                        print(f"[SkillGenerator] Error archiving skill '{name}': {e}")
        
        if archived_count > 0:
            self._save_usage()
            
        return archived_count
