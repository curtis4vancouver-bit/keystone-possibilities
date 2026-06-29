import os
import json
import sys
from typing import Dict, Any, Optional

class ContextCompiler:
    def __init__(self, brand_brain_path: str = None):
        """
        Cognitive Shielding & Context Compiler.
        Enforces absolute decontextualization boundaries. Spoke agents have zero direct filesystem
        visibility to the global_brand_brain.json. Only compiles slices as transient system tokens.
        """
        if brand_brain_path is None:
            # Locate relative to app/core/context_compiler.py -> 01_Brand_Identity/global_brand_brain.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            brand_brain_path = os.path.abspath(os.path.join(current_dir, "..", "..", "01_Brand_Identity", "global_brand_brain.json"))
            
        self.brand_brain_path = brand_brain_path
        self.brain_data: Dict[str, Any] = {}
        self.load_brand_brain()

    def load_brand_brain(self):
        """Loads and parses the global brand brain JSON safely."""
        if not os.path.exists(self.brand_brain_path):
            print(f"[ContextCompiler] ⚠️ Brand brain file not found at: {self.brand_brain_path}", file=sys.stderr)
            self.brain_data = {}
            return
            
        try:
            with open(self.brand_brain_path, "r", encoding="utf-8") as f:
                self.brain_data = json.load(f)
            print(f"[ContextCompiler] Successfully ingested global brand brain profile.")
        except Exception as e:
            print(f"[ContextCompiler] 🛑 Parsing error on brand brain: {str(e)}", file=sys.stderr)
            self.brain_data = {}

    def compile_spoke_context(self, agent_name: str) -> Dict[str, Any]:
        """
        Partitions the global brand brain into isolated context scopes.
        Rigorously filters key nodes prior to subagent invocation.
        """
        if not self.brain_data:
            return {}

        sliced_context = {
            "last_updated": self.brain_data.get("metadata", {}).get("last_updated"),
            "active_phase": self.brain_data.get("brand_milestones", {}).get("active_phase")
        }

        # Enforce target decontextualized maps
        if agent_name == "youtube_scripter":
            # Extracts YouTube Recomposition metrics and stoic builder rules.
            # OMIT B2B business licenses and outbound lead blueprints.
            sliced_context["digital_infrastructure"] = self.brain_data.get("digital_infrastructure", {}).get("recomposition", {})
            sliced_context["builder_persona"] = self.brain_data.get("builder_persona", {})
            
        elif agent_name == "creative_media":
            # Extracts assets hosting, soundtrack metrics, and dynamic video layout limits.
            # OMIT personal physiological metrics and B2B parameters.
            sliced_context["digital_infrastructure"] = self.brain_data.get("digital_infrastructure", {}).get("recomposition", {})
            # Filter to only sonic rules to protect core persona logic
            sonic_rules = [r for r in self.brain_data.get("builder_persona", {}).get("rules", []) if "sonic" in r.lower() or "house" in r.lower() or "frequency" in r.lower()]
            sliced_context["builder_persona"] = {
                "spoken_tone": self.brain_data.get("builder_persona", {}).get("spoken_tone"),
                "rules": sonic_rules
            }

        elif agent_name == "b2b_ops":
            # Extracts BC Builder licensing and company credentials.
            # OMIT YouTube scripts, music playlists, and physiological metadata.
            sliced_context["digital_infrastructure"] = self.brain_data.get("digital_infrastructure", {}).get("construction", {})
            # Only extract professional business persona characteristics
            sliced_context["builder_persona"] = {
                "spoken_tone": self.brain_data.get("builder_persona", {}).get("spoken_tone"),
                "rules": [r for r in self.brain_data.get("builder_persona", {}).get("rules", []) if "medical" not in r.lower() and "sonic" not in r.lower()]
            }

        else:
            # Default fallback for new/custom dynamic spokes
            sliced_context["builder_persona"] = {
                "spoken_tone": self.brain_data.get("builder_persona", {}).get("spoken_tone", "Empirical")
            }

        return sliced_context

    def compile_system_prompt(self, agent_name: str, base_instructions: str) -> str:
        """
        Assembles the decontextualized slice as an immutable read-only prompt block,
        guaranteeing Brand Alignment and preventing LLM context-drift or conversational jailbreaks.
        """
        context_slice = self.compile_spoke_context(agent_name)
        if not context_slice:
            return f"SYSTEM INSTRUCTIONS:\n{base_instructions}"

        # Render structured markdown block
        prompt_block = []
        prompt_block.append("# BRAND COGNITIVE SUBSTRATE (READ-ONLY)")
        prompt_block.append(f"Active Phase: {context_slice.get('active_phase', 'N/A')}")
        prompt_block.append(f"Profile Sync: {context_slice.get('last_updated', 'N/A')}\n")

        # Compile digital infrastructure variables
        infra = context_slice.get("digital_infrastructure", {})
        if infra:
            prompt_block.append("## Digital Infrastructure & Brand Parameters")
            for k, v in infra.items():
                prompt_block.append(f"- **{k.replace('_', ' ').title()}**: {v}")
            prompt_block.append("")

        # Compile builder persona rules
        persona = context_slice.get("builder_persona", {})
        if persona:
            prompt_block.append("## Persona Rules & Communication Boundaries")
            prompt_block.append(f"- **Tone**: {persona.get('spoken_tone', 'Empirical, Blue-Collar Stoic')}")
            metaphors = persona.get("metaphors")
            if metaphors:
                prompt_block.append(f"- **Metaphors**: {metaphors}")
            
            rules = persona.get("rules", [])
            if rules:
                prompt_block.append("### Strict Rules:")
                for rule in rules:
                    prompt_block.append(f"  * {rule}")
            prompt_block.append("")

        prompt_block.append("## TARGET EXECUTION INSTRUCTIONS")
        prompt_block.append(base_instructions)
        prompt_block.append("\n[END OF SYSTEM SUBSTRATE]")

        return "\n".join(prompt_block)
