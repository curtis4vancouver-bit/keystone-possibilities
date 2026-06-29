import json, os
with open(r'C:\Users\Curtis\.gemini\antigravity\brain\e5e3ce7c-557f-4799-9194-c05a03f72bf0\.system_generated\steps\187\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('[')
end = text.rfind(']') + 1
data = json.loads(text[start:end])
full = [d for d in data if d.get('length', 0) >= 20]
with open('SCRAPED_GOOGLE_DOCS.md', 'w', encoding='utf-8') as out:
    out.write('# Scraped Google Docs Data\n\n')
    for d in full:
        out.write(f'## {d["title"]}\n\n{d["text"]}\n\n---\n\n')
print('Done!')
