import re

class TaskRouter:
    def __init__(self):
        # 13 routing categories mapping to agents
        self.rules = {
            "chronos_master": {
                "keywords": ["orchestrate", "master brain", "system status", "health check", "loop", "coordinate"],
                "skill": "01_chronos_master_brain"
            },
            "possibilities_brand": {
                "keywords": ["possibilities", "construction video", "script", "omi", "bill 44", "project management content"],
                "skill": "02_possibilities_brand"
            },
            "local_seo": {
                "keywords": ["local seo", "gmb", "sea-to-sky", "squamish", "whistler", "citation", "ranking"],
                "skill": "04_keystone_local_seo"
            },
            "protocol_brand": {
                "keywords": ["protocol", "peptide", "health", "wellness", "tirzepatide", "bpc-157", "script studio"],
                "skill": "05_protocol_script_studio"
            },
            "music_brand": {
                "keywords": ["music", "recomposition music", "spotify", "lyrics", "avatar generation", "binaural"],
                "skill": "08_music_brand"
            },
            "recomposition_music": {
                "keywords": ["distribution", "streaming optimization", "toolost"],
                "skill": "08_music_brand"
            },
            "webmaster": {
                "keywords": ["website", "landing page", "google console", "knowledge panel", "backlink", "wordpress"],
                "skill": "11_webmaster"
            },
            "legal_counsel": {
                "keywords": ["legal", "contract", "dispute", "compliance", "law"],
                "skill": "12_legal_counsel"
            },
            "tax_strategist": {
                "keywords": ["tax", "deduction", "financial", "accounting", "cra"],
                "skill": "13_tax_strategist"
            },
            "site_superintendent": {
                "keywords": ["job site", "blueprint", "step code", "construction compliance", "site management"],
                "skill": "15_site_superintendent"
            },
            "research_scout": {
                "keywords": ["research", "discover", "threat", "opportunity", "deep dive"],
                "skill": "16_research_scout"
            },
            "analytics_reporting": {
                "keywords": ["analytics", "report", "performance", "youtube metrics", "data pull"],
                "skill": "17_analytics_reporting"
            },
            "executive_assistant": {
                "keywords": ["email", "gmail", "schedule", "personal ea", "draft reply"],
                "skill": "18_executive_assistant"
            }
        }
        
        # Pre-compile regex for speed
        self.compiled_rules = {}
        for agent, data in self.rules.items():
            pattern = r"\b(" + "|".join(map(re.escape, data["keywords"])) + r")\b"
            self.compiled_rules[agent] = {
                "regex": re.compile(pattern, re.IGNORECASE),
                "skill": data["skill"]
            }

    def route(self, task_description: str) -> dict:
        best_agent = None
        best_skill = None
        max_hits = 0
        
        for agent, data in self.compiled_rules.items():
            hits = len(data["regex"].findall(task_description))
            if hits > max_hits:
                max_hits = hits
                best_agent = agent
                best_skill = data["skill"]
                
        # Calculate confidence based on hits. Max hits assumed 5 for 1.0 confidence.
        confidence = min(max_hits / 3.0, 1.0)
        
        return {
            "agent": best_agent,
            "skill": best_skill,
            "confidence": confidence,
            "needs_llm_routing": confidence < 0.5,
            "hits": max_hits
        }

    def route_batch(self, tasks: list[str]) -> list[dict]:
        return [self.route(task) for task in tasks]

if __name__ == "__main__":
    router = TaskRouter()
    print(router.route("I need to write a script for a construction video about bill 44"))
    print(router.route("Check my gmail and schedule a meeting"))

