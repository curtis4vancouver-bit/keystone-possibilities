import os
import sys
import asyncio

# Setup module pathing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.agent_registry import AgentRegistry
from app.core.context_compiler import ContextCompiler
from app.core.a2a_server import A2AServer, AgentCard, TaskRequest, TextPart
from app.core.a2a_client import A2AClient
from app.core.watchdog import WatchdogDaemon

def test_registry():
    print("[TEST] 1. Initializing AgentRegistry...")
    registry = AgentRegistry()
    spokes = registry.list_spokes()
    assert len(spokes) == 3, f"Expected 3 spokes, discovered {len(spokes)}"
    print(f"[TEST] [OK] Discovered spokes successfully: {[s['agent_name'] for s in spokes]}")
    
    # Assert provisioned folders exist
    scripter_ws = os.path.expanduser("~/.chronos/workspaces/youtube_scripter")
    assert os.path.exists(scripter_ws), "YouTube Scripter workspace directory not provisioned!"
    assert os.path.exists(os.path.join(scripter_ws, "db")), "db subfolder not provisioned!"
    print("[TEST] [OK] Workspace folder structures created successfully under NTFS.")

def test_context_compiler():
    print("[TEST] 2. Initializing ContextCompiler...")
    compiler = ContextCompiler()
    
    # 2a. YouTube Scripter partition
    scripter_context = compiler.compile_spoke_context("youtube_scripter")
    assert "builder_persona" in scripter_context, "Persona missing in Scripter context"
    assert "spoken_tone" in scripter_context["builder_persona"], "Tone missing in Scripter context"
    # Ensure business licenses are omitted
    assert "builder_license" not in scripter_context.get("digital_infrastructure", {}), "Leaks builder license to YouTube Scripter!"
    print("[TEST] [OK] YouTube Scripter brand brain partition isolated successfully.")
    
    # 2b. B2B Ops partition
    b2b_context = compiler.compile_spoke_context("b2b_ops")
    assert "builder_license" in b2b_context.get("digital_infrastructure", {}), "Builder license missing in B2B context"
    # Ensure sonic Progressive Tech House music rules are omitted
    sonic_rules = [r for r in b2b_context["builder_persona"].get("rules", []) if "sonic" in r.lower()]
    assert len(sonic_rules) == 0, "Leaks music rules to B2B!"
    print("[TEST] [OK] B2B Operations brand brain partition isolated successfully.")
    
    # 2c. System prompt compilation
    sys_prompt = compiler.compile_system_prompt("youtube_scripter", "Produce a 5 minute script.")
    assert "BRAND COGNITIVE SUBSTRATE" in sys_prompt
    assert "Produce a 5 minute script." in sys_prompt
    print("[TEST] [OK] Secure system prompt context generated successfully.")

def test_models():
    print("[TEST] 3. Testing Pydantic serialization...")
    # Validate TextPart models
    part = TextPart(text="Hardcore biological recomposition draft")
    assert part.type == "text"
    
    card = AgentCard(
        agent_name="youtube_scripter",
        port=8001,
        capabilities=["scriptwriting"],
        description="Empirical scripter",
        rules=["Include disclaimer"]
    )
    assert card.status == "idle"
    print("[TEST] [OK] Message parts and AgentCard schema models verified.")

async def test_watchdog():
    print("[TEST] 4. Initializing WatchdogDaemon...")
    daemon = WatchdogDaemon()
    await daemon.start()
    assert daemon.running == True
    print("[TEST] [OK] Watchdog background telemetry daemon initialized and started.")
    await daemon.stop()
    assert daemon.running == False
    print("[TEST] [OK] Watchdog stopped gracefully.")

async def main():
    print("====================================================")
    print(" RUNNING CHRONOS AGENT OS CORE SYSTEM TESTING      ")
    print("====================================================")
    
    try:
        test_registry()
        test_context_compiler()
        test_models()
        await test_watchdog()
        print("====================================================")
        print(" SUCCESS: ALL CHRONOS CORE MODULES PASSED SANITY    ")
        print("====================================================")
    except AssertionError as ae:
        print(f"[TEST FAILED] Assertion failed: {ae}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[TEST FAILED] Execution crashed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
