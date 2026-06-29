import os
import sys
import glob
import yaml
from typing import Dict, Any, List, Optional

class AgentRegistry:
    def __init__(self, spokes_dir: str = None):
        """
        Initializes the AgentRegistry.
        By default, scans the sibling 'spokes' folder in the package structure.
        """
        if spokes_dir is None:
            # Locate relative to app/core/agent_registry.py -> app/spokes/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            spokes_dir = os.path.abspath(os.path.join(current_dir, "..", "spokes"))
        
        self.spokes_dir = spokes_dir
        self.registry: Dict[str, Dict[str, Any]] = {}
        os.makedirs(self.spokes_dir, exist_ok=True)
        self.scan_and_load_spokes()

    def scan_and_load_spokes(self) -> Dict[str, Dict[str, Any]]:
        """
        Scans app/spokes/*.yaml and dynamically registers active Spokes.
        """
        pattern = os.path.join(self.spokes_dir, "*.yaml")
        yaml_files = glob.glob(pattern)
        
        discovered: Dict[str, Dict[str, Any]] = {}
        for y_path in yaml_files:
            try:
                with open(y_path, "r", encoding="utf-8") as f:
                    card = yaml.safe_load(f)
                    if card and "agent_name" in card:
                        name = card["agent_name"]
                        # Auto-resolve workspace path in Windows if ~ is used
                        ws_dir = card.get("workspace_dir", f"~/.chronos/workspaces/{name}")
                        resolved_ws = os.path.abspath(os.path.expanduser(ws_dir))
                        card["workspace_dir"] = resolved_ws
                        
                        discovered[name] = card
                        # Auto-provision workspace structure on discovery
                        self.provision_workspace(name, resolved_ws)
            except Exception as e:
                print(f"[AgentRegistry] Error parsing yaml '{y_path}': {str(e)}", file=sys.stderr)
        
        self.registry = discovered
        return self.registry

    def register_spoke_dynamically(self, card: Dict[str, Any]) -> bool:
        """
        Registers a new spoke dynamically.
        Writes its configuration file to app/spokes/<name>.yaml and loads it.
        """
        name = card.get("agent_name")
        if not name:
            return False
            
        # Ensure default ports and pathways if omitted
        if "port" not in card:
            # Dynamically allocate next port
            existing_ports = [spk.get("port") for spk in self.registry.values() if spk.get("port")]
            next_port = max(existing_ports) + 1 if existing_ports else 8001
            card["port"] = next_port
            
        ws_dir = card.get("workspace_dir", f"~/.chronos/workspaces/{name}")
        resolved_ws = os.path.abspath(os.path.expanduser(ws_dir))
        card["workspace_dir"] = resolved_ws
        
        # Write back to disk so discovery is persistent
        target_path = os.path.join(self.spokes_dir, f"{name}.yaml")
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(card, f, default_flow_style=False)
            
            # Re-provision workspace
            self.provision_workspace(name, resolved_ws)
            # Reload
            self.scan_and_load_spokes()
            return True
        except Exception as e:
            print(f"[AgentRegistry] Dynamic registration failed for {name}: {str(e)}", file=sys.stderr)
            return False

    def provision_workspace(self, agent_name: str, path: str):
        """
        Automatically generates isolated directories, database spaces, and structure paths.
        Guarantees Windows NTFS-safe folder initialization.
        """
        subfolders = ["db", "local_locked", "Research_Archives", "Transcripts", "scratch"]
        for sf in subfolders:
            sf_path = os.path.join(path, sf)
            os.makedirs(sf_path, exist_ok=True)
        
        # Touch initialization files
        init_marker = os.path.join(path, ".chronos_initialized")
        if not os.path.exists(init_marker):
            with open(init_marker, "w", encoding="utf-8") as f:
                f.write(f"Chronos workspace active. Name: {agent_name}\nCreated: {os.path.getctime(path)}")
        print(f"[AgentRegistry] Provisioned workspace for '{agent_name}' under: {path}")

    def get_spoke_card(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves active details of a registered Spoke.
        """
        return self.registry.get(agent_name)

    def list_spokes(self) -> List[Dict[str, Any]]:
        """
        Lists all registered Spoke cards.
        """
        return list(self.registry.values())
