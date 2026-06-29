import os, json, re

registry = {'version': '2026-06-10', 'skills': []}
dirs = {
    'global': r'C:\Users\Curtis\.gemini\config\skills',
    'workspace': r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skills'
}

for loc, path in dirs.items():
    if not os.path.exists(path): continue
    for d in os.listdir(path):
        skill_dir = os.path.join(path, d)
        if os.path.isdir(skill_dir):
            skill_md = os.path.join(skill_dir, 'SKILL.md')
            if os.path.exists(skill_md):
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    name_match = re.search(r'name:\s*(.+)', content)
                    desc_match = re.search(r'description:\s*(?:\"(.*?)\"|(.+))', content)
                    if name_match:
                        name = name_match.group(1).strip()
                        desc = ''
                        if desc_match:
                            desc = desc_match.group(1) or desc_match.group(2)
                            desc = desc.strip()
                        auto_load = True if name in ['keystone-session-bootstrap', '00_keystone_foundation'] else False
                        registry['skills'].append({
                            'name': name,
                            'location': loc,
                            'description': desc,
                            'auto_load': auto_load
                        })

with open(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skill_registry.json', 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=2)
print('Registry built with {} skills.'.format(len(registry['skills'])))
