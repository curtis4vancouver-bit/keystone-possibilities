import sys as _sys
_sys.stdout.reconfigure(encoding='utf-8', errors='replace')
"""
Keystone Unified Agent Orchestrator
====================================
Integrates three Gemini capabilities into a single callable system:

1. COMPUTER USE  — Visual desktop automation via gemini-3.5-flash
2. ANTIGRAVITY AGENT — Cloud-hosted autonomous coding/research agent  
3. DEEP RESEARCH — Multi-page web research compilation

All three share the same API key from .env and can be called
by Antigravity (the IDE agent) or by each other.
"""

import os
import sys
import json
import time
import base64
import threading
from dotenv import load_dotenv
from google import genai

# Load environment
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

class KeystoneOrchestrator:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("No GEMINI_API_KEY found in .env")
        self.client = genai.Client(api_key=api_key)
        self.results_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Agent_Fleet", "orchestrator_results"
        )
        os.makedirs(self.results_dir, exist_ok=True)
        print(f"[Orchestrator] Initialized with API key {api_key[:8]}...")
        print(f"[Orchestrator] Results directory: {self.results_dir}")

    # ──────────────────────────────────────────────
    # 1. COMPUTER USE — Visual Desktop Automation
    # ──────────────────────────────────────────────
    def computer_use(self, goal: str, screenshot_bytes: bytes = None, max_steps: int = 15):
        """
        Send a screenshot + goal to Gemini 3.5 Flash with computer_use tool.
        Returns the list of action steps the model wants to execute.
        If no screenshot_bytes provided, tries to capture the screen.
        """
        print(f"\n[Computer Use] Goal: '{goal}'")
        
        if screenshot_bytes is None:
            try:
                import mss
                from PIL import Image
                import io
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    sct_img = sct.grab(monitor)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    screenshot_bytes = buf.getvalue()
            except Exception as e:
                print(f"[Computer Use] Screen capture failed: {e}")
                return {"error": str(e)}
        
        encoded = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        try:
            response = self.client.interactions.create(
                model="gemini-3.5-flash",
                input=[
                    {"type": "text", "text": f"Goal: {goal}"},
                    {"type": "image", "data": encoded, "mime_type": "image/png"}
                ],
                tools=[{"type": "computer_use", "environment": "desktop"}]
            )
            
            steps = []
            for s in getattr(response, "steps", []):
                if getattr(s, "type", "") == "function_call":
                    steps.append({
                        "action": getattr(s, "name", ""),
                        "arguments": getattr(s, "arguments", {}),
                        "id": getattr(s, "id", "")
                    })
            
            usage = getattr(response, "usage", None)
            tokens_used = getattr(usage, "total_tokens", 0) if usage else 0
            
            result = {
                "status": getattr(response, "status", "unknown"),
                "steps": steps,
                "tokens_used": tokens_used,
                "interaction_id": getattr(response, "id", "")
            }
            print(f"[Computer Use] Got {len(steps)} action(s), used {tokens_used} tokens")
            return result
            
        except Exception as e:
            print(f"[Computer Use] Error: {e}")
            return {"error": str(e)}

    # ──────────────────────────────────────────────
    # 2. ANTIGRAVITY AGENT — Cloud Coding Agent
    # ──────────────────────────────────────────────
    def run_agent(self, task: str, background: bool = False):
        """
        Spin up a cloud-hosted Antigravity agent to perform a coding,
        analysis, or research task. Returns the agent's output.
        """
        print(f"\n[Antigravity Agent] Task: '{task}'")
        print(f"[Antigravity Agent] Background: {background}")
        
        try:
            response = self.client.interactions.create(
                agent="antigravity-preview-05-2026",
                input=task,
                environment="remote",
                background=background
            )
            
            if background:
                interaction_id = getattr(response, "id", "")
                print(f"[Antigravity Agent] Started in background: {interaction_id}")
                return {"status": "running", "interaction_id": interaction_id}
            
            output = getattr(response, "output_text", "")
            usage = getattr(response, "usage", None)
            tokens_used = getattr(usage, "total_tokens", 0) if usage else 0
            
            result = {
                "status": getattr(response, "status", "completed"),
                "output": output,
                "tokens_used": tokens_used,
                "interaction_id": getattr(response, "id", "")
            }
            
            # Save result to file
            result_file = os.path.join(self.results_dir, f"agent_{int(time.time())}.json")
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"[Antigravity Agent] Completed. Tokens: {tokens_used}")
            print(f"[Antigravity Agent] Output saved to: {result_file}")
            return result
            
        except Exception as e:
            print(f"[Antigravity Agent] Error: {e}")
            return {"error": str(e)}

    def poll_agent(self, interaction_id: str):
        """Poll a background agent task for completion."""
        try:
            response = self.client.interactions.get(id=interaction_id)
            status = getattr(response, "status", "unknown")
            output = getattr(response, "output_text", "")
            return {"status": status, "output": output}
        except Exception as e:
            return {"error": str(e)}

    # ──────────────────────────────────────────────
    # 3. DEEP RESEARCH — Multi-page Web Research
    # ──────────────────────────────────────────────
    def deep_research(self, query: str):
        """
        Run a deep research query using Google's hosted deep research model.
        Returns a comprehensive research report.
        """
        print(f"\n[Deep Research] Query: '{query}'")
        
        try:
            response = self.client.interactions.create(
                agent="antigravity-preview-05-2026",
                input=query,
                agent_config={"deep_research": True},
                environment="remote"
            )
            
            output = getattr(response, "output_text", "")
            usage = getattr(response, "usage", None)
            tokens_used = getattr(usage, "total_tokens", 0) if usage else 0
            
            # Save research report
            report_file = os.path.join(self.results_dir, f"research_{int(time.time())}.md")
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(f"# Deep Research: {query}\n\n")
                f.write(output)
            
            result = {
                "status": "completed",
                "output": output,
                "tokens_used": tokens_used,
                "report_file": report_file
            }
            print(f"[Deep Research] Completed. Tokens: {tokens_used}")
            print(f"[Deep Research] Report saved to: {report_file}")
            return result
            
        except Exception as e:
            print(f"[Deep Research] Error: {e}")
            return {"error": str(e)}

    # ──────────────────────────────────────────────
    # HEALTH CHECK — Verify all three capabilities
    # ──────────────────────────────────────────────
    def health_check(self):
        """Verify API connectivity for all three capabilities."""
        print("\n" + "=" * 60)
        print("  KEYSTONE ORCHESTRATOR HEALTH CHECK")
        print("=" * 60)
        
        results = {}
        
        # 1. Test Computer Use (with dummy image)
        print("\n[1/3] Testing Computer Use (gemini-3.5-flash)...")
        from PIL import Image
        import io
        dummy = Image.new("RGB", (100, 100), (200, 200, 200))
        buf = io.BytesIO()
        dummy.save(buf, format="PNG")
        cu_result = self.computer_use("Describe what you see", buf.getvalue(), max_steps=1)
        results["computer_use"] = "error" not in cu_result
        status = "[PASS]" if results["computer_use"] else "[FAIL]"
        print(f"    {status}")
        
        # Brief pause to avoid rate limits between tests
        time.sleep(3)
        
        # 2. Test Antigravity Agent
        print("\n[2/3] Testing Antigravity Agent (antigravity-preview-05-2026)...")
        try:
            ag_response = self.client.interactions.create(
                agent="antigravity-preview-05-2026",
                input="Say 'health check passed' and nothing else.",
                environment="remote"
            )
            ag_output = getattr(ag_response, "output_text", "")
            results["antigravity_agent"] = len(ag_output) > 0
        except Exception as e:
            results["antigravity_agent"] = False
            print(f"    Error: {e}")
        status = "[PASS]" if results["antigravity_agent"] else "[FAIL]"
        print(f"    {status}")
        
        # 3. Test Deep Research model availability
        print("\n[3/3] Testing Deep Research model availability...")
        try:
            models = [m.name for m in self.client.models.list() if 'deep-research' in m.name]
            results["deep_research"] = len(models) > 0
            if models:
                print(f"    Available models: {', '.join(models)}")
        except Exception as e:
            results["deep_research"] = False
            print(f"    Error: {e}")
        status = "[PASS]" if results["deep_research"] else "[FAIL]"
        print(f"    {status}")
        
        # Summary
        print("\n" + "=" * 60)
        all_pass = all(results.values())
        if all_pass:
            print("  ALL SYSTEMS OPERATIONAL")
        else:
            failed = [k for k, v in results.items() if not v]
            print(f"  FAILED: {', '.join(failed)}")
        print("=" * 60)
        
        return results


def main():
    orch = KeystoneOrchestrator()
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python keystone_orchestrator.py health       — Run health check")
        print("  python keystone_orchestrator.py computer     — Computer Use test")
        print("  python keystone_orchestrator.py agent <task> — Run Antigravity Agent")
        print("  python keystone_orchestrator.py research <q> — Run Deep Research")
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "health":
        orch.health_check()
    elif cmd == "computer":
        goal = sys.argv[2] if len(sys.argv) > 2 else "Describe what you see on screen"
        result = orch.computer_use(goal)
        print(json.dumps(result, indent=2, default=str))
    elif cmd == "agent":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Say hello"
        result = orch.run_agent(task)
        print(json.dumps(result, indent=2, default=str))
    elif cmd == "research":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Latest AI developments"
        result = orch.deep_research(query)
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
