import json

path = r"C:\Users\Curtis\.gemini\antigravity\brain\231c6914-89c5-4c61-99bf-e20300ea490f\.system_generated\logs\transcript.jsonl"
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        if "send_message" in line:
            print("Found line with send_message:")
            d = json.loads(line)
            print("Keys:", d.keys())
            if "tool_calls" in d:
                for tc in d["tool_calls"]:
                    print("Tool:", tc.get("name"))
                    print("Args:", list(tc.get("args", {}).keys()))
                    # print content of message
                    msg = tc.get("args", {}).get("Message", "")
                    print("Message length:", len(msg))
                    with open("scratch/subagent_message.txt", "w", encoding="utf-8") as out:
                        out.write(msg)
                    print("Wrote message to scratch/subagent_message.txt")
            elif "content" in d:
                print("Content:", d["content"][:200])
            print("="*40)
