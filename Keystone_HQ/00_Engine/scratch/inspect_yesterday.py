import json

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        try:
            step = json.loads(line)
            tool_calls = step.get("tool_calls", [])
            for tc in tool_calls:
                name = tc.get("name")
                if name in ["type_text", "click", "evaluate_script"]:
                    args = tc.get("args", {})
                    # If it's related to Flow
                    args_str = str(args)
                    if "whip-pan" in args_str or "Ana" in args_str or "Create" in args_str or "Enter" in args_str:
                        print(f"Step {step.get('step_index')}: {name} | {args_str[:160]}")
                        count += 1
                        if count > 40:
                            break
            if count > 40:
                break
        except Exception:
            pass
