import re
import os

md_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md"
js_out = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\submit_prompts.js"

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# We want to find all clip prompts from A2 to A24
# Clips are defined as:
# ### CLIP A[2-24] ...
# ```
# [prompt]
# ```
prompts = []
for i in range(2, 25):
    pattern = rf"### CLIP A{i}.*?\n```\n(.*?)\n```"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        prompt_text = match.group(1).strip().replace("\n", " ").replace('"', '\\"')
        prompts.append(prompt_text)
        print(f"Found A{i} prompt: {prompt_text[:60]}...")
    else:
        print(f"WARNING: Could not find prompt for A{i}!")

# Verify count
print(f"Total parsed prompts (A2-A24): {len(prompts)}")

# Now we write the JS script
js_code = f"""async () => {{
  const prompts = [
"""

for p in prompts:
    js_code += f'    "{p}",\n'

js_code += """  ];
  
  function clickEl(el) {
    const events = ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'];
    events.forEach(type => {
      el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window }));
    });
  }
  
  const results = [];
  
  for (let idx = 0; idx < prompts.length; idx++) {
    const promptText = prompts[idx];
    const clipNum = idx + 2;
    console.log(`Submitting clip A${clipNum}...`);
    
    // 1. Click "+ Create" button
    const buttons = Array.from(document.querySelectorAll('button'));
    const plusBtn = buttons.find(b => b.innerText && b.innerText.includes('add_2') && b.innerText.includes('Create'));
    if (!plusBtn) {
      results.push({ clip: `A${clipNum}`, status: "Error: + Create button not found" });
      continue;
    }
    plusBtn.click();
    
    // 2. Poll for Characters tab
    let charTab = null;
    for (let i = 0; i < 30; i++) {
      const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
      charTab = tabs.find(t => t.innerText && t.innerText.includes('Characters'));
      if (charTab) break;
      await new Promise(r => setTimeout(r, 100));
    }
    if (!charTab) {
      results.push({ clip: `A${clipNum}`, status: "Error: Characters tab not found" });
      continue;
    }
    charTab.click();
    
    // 3. Poll for Ana Stevenson card
    let anaEl = null;
    for (let i = 0; i < 30; i++) {
      const elements = Array.from(document.querySelectorAll('*'));
      anaEl = elements.find(el => el.innerText === 'Ana Stevenson');
      if (anaEl) break;
      await new Promise(r => setTimeout(r, 100));
    }
    if (!anaEl) {
      results.push({ clip: `A${clipNum}`, status: "Error: Ana Stevenson element not found in dialog" });
      continue;
    }
    anaEl.click();
    
    // 4. Poll for Add to Prompt button
    let addBtn = null;
    for (let i = 0; i < 30; i++) {
      addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText === 'Add to Prompt');
      if (addBtn) break;
      await new Promise(r => setTimeout(r, 100));
    }
    if (!addBtn) {
      results.push({ clip: `A${clipNum}`, status: "Error: Add to Prompt button not found" });
      continue;
    }
    addBtn.click();
    
    // 5. Wait for dialog to close
    await new Promise(r => setTimeout(r, 400));
    
    // 6. Focus editor and type text
    const editor = document.querySelector('div[contenteditable="true"]');
    if (!editor) {
      results.push({ clip: `A${clipNum}`, status: "Error: Editor not found" });
      continue;
    }
    editor.focus();
    editor.innerText = promptText;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    
    // 7. Wait for submit button to enable
    let submitBtn = null;
    for (let i = 0; i < 30; i++) {
      const btns = Array.from(document.querySelectorAll('button'));
      submitBtn = btns.find(b => b.innerText && b.innerText.includes('Create') && b.innerText.includes('arrow_forward'));
      if (submitBtn && !submitBtn.disabled) break;
      await new Promise(r => setTimeout(r, 100));
    }
    if (!submitBtn || submitBtn.disabled) {
      results.push({ clip: `A${clipNum}`, status: "Error: Submit button disabled or missing" });
      continue;
    }
    
    submitBtn.click();
    results.push({ clip: `A${clipNum}`, status: "Success" });
    
    // 8. Wait between generations
    await new Promise(r => setTimeout(r, 1000));
  }
  
  return results;
}"""

with open(js_out, "w", encoding="utf-8") as f:
    f.write(js_code)

print(f"Generated JS automation script at: {js_out}")
