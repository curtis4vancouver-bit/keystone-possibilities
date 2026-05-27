import os
import glob
import re

html_files = glob.glob('*.html')
subscribe_html = """
            <!-- Global Subscribe Buttons -->
            <div class="keystone-global-subscribe-buttons" style="display:flex; flex-wrap:wrap; gap:15px; margin-top:40px; margin-bottom: 40px; justify-content: center; align-items: center;">
                <a href="https://www.youtube.com/@keystonerecomposition?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: 'Outfit', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">▶ Subscribe: Keystone Recomposition</a>
                <a href="https://www.youtube.com/@keystoneprotocols?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: 'Outfit', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">▶ Subscribe: Keystone Protocols</a>
            </div>
"""

for file_path in html_files:
    if file_path in ['index.html', 'page.html']:
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'Subscribe: Keystone Recomposition' not in content:
        # First, remove the old single "Subscribe Channel" bar if it exists so we don't have duplicates
        # But wait, the old bar has nice text like "KEYSTONE YOUTUBE TRANSMISSIONS".
        # Let's just inject the new buttons right before </main> for simplicity and maximum visibility.
        
        if '</main>' in content:
            new_content = content.replace('</main>', subscribe_html + '\n        </main>')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected dual buttons into {file_path}")
        else:
            print(f"Could not find </main> in {file_path}")
    else:
        print(f"Dual buttons already in {file_path}")
