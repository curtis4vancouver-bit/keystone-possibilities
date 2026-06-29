import json
import os

step_3602_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3602\output.txt"
if os.path.exists(step_3602_path):
    print("Step 3602 output.txt exists!")
    with open(step_3602_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"Length of step 3602 output: {len(content)}")
    print("Snippet (first 1000 chars):")
    print(content[:1000])
    
    # Try to parse as JSON and print fields
    content_stripped = content.strip()
    if "Script ran on page and returned:\n" in content_stripped:
        content_stripped = content_stripped.replace("Script ran on page and returned:\n", "")
    
    # Remove code fences
    if content_stripped.startswith("```json"):
        content_stripped = content_stripped.replace("```json", "", 1)
        if content_stripped.endswith("```"):
            content_stripped = content_stripped[:-3]
    content_stripped = content_stripped.strip()
    
    try:
        data = json.loads(content_stripped)
        print("\nParsed JSON successfully!")
        print("isFinished:", data.get("isFinished"))
        print("bodyLength:", data.get("bodyLength"))
        print("reportLength:", data.get("reportLength"))
        print("reportPreview:")
        print(data.get("reportPreview"))
    except Exception as e:
        print("\nJSON parse failed:", e)
else:
    print("Step 3602 output.txt does not exist.")
