about_md_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\steps\237\content.md"

with open(about_md_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r"(founder|the foreman|wayne stevenson|the founder)", text, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences:")
for m_idx in matches:
    start = max(0, m_idx - 100)
    end = min(len(text), m_idx + 300)
    print(f"\n--- Context at index {m_idx} ---")
    print(text[start:end])
