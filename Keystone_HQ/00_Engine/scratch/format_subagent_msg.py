import json

path = r"C:\Users\Curtis\.gemini\antigravity\brain\231c6914-89c5-4c61-99bf-e20300ea490f\.system_generated\logs\transcript.jsonl"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

messages = []
for idx, line in enumerate(lines):
    if "send_message" in line:
        try:
            d = json.loads(line)
            if "tool_calls" in d:
                for tc in d["tool_calls"]:
                    if tc.get("name") == "send_message":
                        msg = tc["args"].get("Message", "")
                        messages.append((idx, len(msg), msg))
        except Exception as e:
            pass

print(f"Found {len(messages)} messages.")
if messages:
    longest = max(messages, key=lambda x: x[1])
    # Decode string escapes if it has literal \n
    msg_content = longest[2]
    # Replace literal \n and \t if they are encoded
    # The simplest way is to evaluate it as a JSON string if it is surrounded by quotes or double escapes
    try:
        # In case the string contains raw backslashes representing newlines
        msg_content = msg_content.encode('utf-8').decode('unicode_escape')
    except Exception as e:
        print("unicode_escape failed, using raw:", e)
        
    with open("scratch/subagent_message_formatted.txt", "w", encoding="utf-8") as out:
        out.write(longest[2]) # Write original first, we will see
    
    # Let's write the decoded version to a separate file
    try:
        decoded_content = longest[2].replace("\\n", "\n").replace("\\t", "\t").replace("\\\"", "\"")
        with open("scratch/subagent_message_decoded.txt", "w", encoding="utf-8") as out:
            out.write(decoded_content)
        print(f"Saved decoded message (length {len(decoded_content)}) to scratch/subagent_message_decoded.txt")
    except Exception as e:
        print("Failed to write decoded version:", e)
