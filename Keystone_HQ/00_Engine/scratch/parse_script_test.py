import re

def parse_clips(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find all clips. We can split by '### 📋 CLIP A'
    clips = re.split(r'### 📋 CLIP A', content)
    parsed_clips = {}
    
    for clip in clips[1:]:
        # Get clip number
        num_match = re.match(r'(\d+)', clip)
        if not num_match:
            continue
        clip_num = int(num_match.group(1))
        
        # Extract the content inside ```text ... ```
        code_block_match = re.search(r'```text\s*(.*?)\s*```', clip, re.DOTALL)
        if not code_block_match:
            print(f"Warning: No code block in Clip A{clip_num}")
            continue
        
        block_text = code_block_match.group(1).strip()
        
        # Parse "THIS IS THE SCRIPT:" and "THIS IS THE VIDEO PROMPT:"
        script_part = ""
        prompt_part = ""
        
        script_match = re.search(r'THIS IS THE SCRIPT:\s*(.*?)\s*(?=THIS IS THE VIDEO PROMPT:|$)', block_text, re.DOTALL)
        if script_match:
            script_part = " ".join(script_match.group(1).strip().splitlines())
        else:
            print(f"Warning: No script part in Clip A{clip_num}")
            
        prompt_match = re.search(r'THIS IS THE VIDEO PROMPT:\s*(.*)', block_text, re.DOTALL)
        if prompt_match:
            prompt_part = " ".join(prompt_match.group(1).strip().splitlines())
        else:
            print(f"Warning: No prompt part in Clip A{clip_num}")
            
        combined = f"{script_part} {prompt_part}".strip()
        parsed_clips[clip_num] = {
            'speaker': 'Wayne' if 'Wayne says:' in script_part else 'Victoria',
            'script': script_part,
            'prompt': prompt_part,
            'combined': combined
        }
        
    return parsed_clips

def parse_brolls(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by '### B'
    parts = re.split(r'### B', content)
    parsed_brolls = {}
    
    for part in parts[1:]:
        # Check if it starts with a number
        num_match = re.match(r'(\d+)', part)
        if not num_match:
            continue
        broll_num = int(num_match.group(1))
        
        # Extract the content inside ``` ... ```
        # It could be ``` or ```text or ```image
        code_block_match = re.search(r'```(?:text|image)?\s*(.*?)\s*```', part, re.DOTALL)
        if not code_block_match:
            continue
            
        prompt_text = " ".join(code_block_match.group(1).strip().splitlines())
        parsed_brolls[broll_num] = prompt_text
        
    return parsed_brolls

if __name__ == '__main__':
    path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production\LONG_005_RETATRUTIDE_BUILDER_VERDICT.md"
    clips = parse_clips(path)
    brolls = parse_brolls(path)
    print(f"Parsed {len(clips)} clips.")
    print(f"Parsed {len(brolls)} B-rolls.")
    for i in range(1, 6):
        if i in clips:
            print(f"\nClip A{i} ({clips[i]['speaker']}):")
            print(f"  Combined: {clips[i]['combined']}")
    for i in range(1, 6):
        if i in brolls:
            print(f"\nB-roll B{i}:")
            print(f"  Prompt: {brolls[i]}")

