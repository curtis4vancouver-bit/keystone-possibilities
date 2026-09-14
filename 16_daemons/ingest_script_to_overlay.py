#!/usr/bin/env python3
"""
================================================================================
INGEST SCRIPT TO OVERLAY — Dynamic Script Parser & Overlay Compiler
================================================================================
File Location: 16_daemons/ingest_script_to_overlay.py
Purpose: Parses any Markdown script file into the exact AVATAR_SCRIPTS and
         BROLL_SCRIPTS schemas required by the Google Flow Overlay HUD (overlay.js).
         Supports both Wayne & Guest video clips and standalone 1-51 B-Roll prompts.
         Updates 05_Keystone_HUD/button_configs/overlays/google_flow/overlay.js
         and triggers live CDP injection via chrome_overlay_daemon (Port 9879).
================================================================================
"""

import os
import re
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

# Enforce UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BRAIN_ROOT = r"c:\Users\Curtis\Desktop\Keystone Brain"
SCRIPTS_DIR = os.path.join(BRAIN_ROOT, "08_Keystone_protocols", "scripts")
OVERLAY_JS_PATH = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "overlay.js")
PAYLOAD_JSON_PATH = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")


def find_latest_script(channel_name: str = None) -> str:
    """Find the newest markdown script across Keystone Possibilities, Protocols, Recomposition, or 00_todays_video_upload."""
    candidates = []
    
    # 1. Keystone Possibilities scripts
    possibilities_dir = os.path.join(BRAIN_ROOT, "06_Keystone_possibilities", "Google_Flow")
    if os.path.exists(possibilities_dir) and (not channel_name or "possibilit" in channel_name.lower()):
        for f in os.listdir(possibilities_dir):
            if f.endswith(".md") and f.lower() != "00_index.md" and "briefing" not in f.lower():
                fp = os.path.join(possibilities_dir, f)
                candidates.append((fp, os.path.getmtime(fp)))

    # 2. Keystone Protocols scripts
    protocols_dir = os.path.join(BRAIN_ROOT, "08_Keystone_protocols", "scripts")
    if os.path.exists(protocols_dir) and (not channel_name or "protocol" in channel_name.lower()):
        for f in os.listdir(protocols_dir):
            if f.endswith(".md") and f.lower() != "00_index.md" and "briefing" not in f.lower():
                fp = os.path.join(protocols_dir, f)
                candidates.append((fp, os.path.getmtime(fp)))
                
    # 3. Keystone Recomposition scripts
    recomposition_dirs = [
        os.path.join(BRAIN_ROOT, "07_Keystone_recomposition", "Google_Flow"),
        os.path.join(BRAIN_ROOT, "07_Keystone_recomposition", "scripts"),
        os.path.join(BRAIN_ROOT, "07_Keystone_recomposition", "content_production")
    ]
    for r_dir in recomposition_dirs:
        if os.path.exists(r_dir) and (not channel_name or "recomposit" in channel_name.lower()):
            for f in os.listdir(r_dir):
                if f.endswith(".md") and f.lower() != "00_index.md" and "briefing" not in f.lower():
                    fp = os.path.join(r_dir, f)
                    candidates.append((fp, os.path.getmtime(fp)))

    # 4. Check 00_todays_video_upload
    todays_dir = os.path.join(BRAIN_ROOT, "00_todays_video_upload")
    if os.path.exists(todays_dir):
        for f in os.listdir(todays_dir):
            if f.endswith(".md") and f.lower() != "00_index.md" and "briefing" not in f.lower():
                fp = os.path.join(todays_dir, f)
                candidates.append((fp, os.path.getmtime(fp)))

    if not candidates:
        raise FileNotFoundError("No markdown scripts found in any channel scripts directories.")
        
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def parse_markdown_script(script_path: str) -> tuple:
    """Parse Markdown script into (clips, brolls) lists."""
    with open(script_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    main_section = content
    short_split = re.split(r'(?m)^##\s+.*(?:COMPANION SHORT|SHORT FUNNEL)', content, flags=re.IGNORECASE)
    if len(short_split) > 1:
        main_section = short_split[0]

    broll_split = re.split(r'(?m)^##\s+.*(?:B-ROLL PICTURE PROMPTS|B-ROLL PROMPTS)', main_section, flags=re.IGNORECASE)
    video_content = broll_split[0]
    broll_content = broll_split[1] if len(broll_split) > 1 else ""

    ref_assets = {}
    bg_m = re.search(r'###\s*Background\s*(?:Prompt)?\s*(?:\(`?background_1`?\)|background_1)?:?\s*\n+([^\n#]+)', content, flags=re.IGNORECASE)
    if bg_m:
        ref_assets["background_1"] = bg_m.group(1).strip(' \t\r\n`"\'')
    cl_m = re.search(r'###\s*Clothing\s*(?:Prompt)?\s*(?:\(`?cloth_1`?\)|cloth_1)?:?\s*\n+([^\n#]+)', content, flags=re.IGNORECASE)
    if cl_m:
        ref_assets["cloth_1"] = cl_m.group(1).strip(' \t\r\n`"\'')

    clips = []
    brolls = []

    # 1. Parse Video Clips (### Clip ...)
    clip_blocks = re.split(r'(?m)^###\s+Clip\s+', video_content)
    for block in clip_blocks[1:]:
        lines = block.strip().split("\n")
        header = lines[0].strip()

        if header.startswith("Short") or header.startswith("S") or "000100" in header or "disclaimer" in header.lower():
            continue

        id_match = re.match(r'(\d+)', header)
        clip_id = id_match.group(1) if id_match else f"{len(clips)+1:06d}"
        title_text = f"Clip {clip_id}: " + re.sub(r'^\d+[\s:\-–—]*', '', header).strip(': ')

        script_text = ""
        camera_text = ""

        in_script = False
        in_camera = False
        script_lines = []
        camera_lines = []

        for line in lines[1:]:
            line_str = line.strip()
            lower_s = line_str.lower()
            if any(lower_s.startswith(p) for p in ["#### script:", "**script:**", "script:", "#### voiceover script:", "**voiceover script:**", "voiceover script:", "**voiceover:**"]):
                in_script = True
                in_camera = False
                rest = re.sub(r'^(####\s*(?:Voiceover\s*)?Script:|\*\*(?:Voiceover\s*)?Script:\*\*|(?:Voiceover\s*)?Script:|\*\*Voiceover:\*\*)\s*', '', line_str, flags=re.IGNORECASE).strip(' "\'\u201c\u201d')
                if rest: script_lines.append(rest)
                continue
            elif any(lower_s.startswith(p) for p in ["#### visual:", "#### camera:", "**visual:**", "**camera:**", "visual:", "camera:", "#### camera prompt:", "**camera prompt:**", "camera prompt:"]):
                in_script = False
                in_camera = True
                rest = re.sub(r'^(####\s*(?:Visual|Camera(?:\s*Prompt)?):|\*\*(?:Visual|Camera(?:\s*Prompt)?):\*\*|(?:Visual|Camera(?:\s*Prompt)?):)\s*', '', line_str, flags=re.IGNORECASE).strip(' "\'\u201c\u201d')
                if rest: camera_lines.append(rest)
                continue
            elif line_str.startswith("### ") or line_str.startswith("## ") or line_str.startswith("---"):
                break

            if in_script:
                cleaned = line_str.strip(' "\'\u201c\u201d')
                if cleaned and not cleaned.startswith("*") and not cleaned.startswith("-"):
                    script_lines.append(cleaned)
            elif in_camera:
                cleaned = line_str.strip(' "\'\u201c\u201d')
                if cleaned and not cleaned.startswith("*") and not cleaned.startswith("-"):
                    camera_lines.append(cleaned)

        # Check for inline format: Presenter says: "..." Camera: ...
        inline_match = re.search(r'Presenter says:\s*["“](.*?)["”]\s+(?:Camera|Visual):\s*(.*)', block, flags=re.DOTALL)
        if inline_match:
            script_text = inline_match.group(1).strip()
            camera_text = inline_match.group(2).strip()
        else:
            script_text = " ".join(script_lines).strip(' "\'\u201c\u201d')
            camera_text = " ".join(camera_lines).strip(' "\'\u201c\u201d')

        header_lower = header.lower()
        camera_lower = camera_text.lower()
        if "scene" in header_lower or "no photo" in header_lower or "pure scene" in header_lower:
            speaker = "scene"
        elif "wayne" in header_lower:
            if "using reference picture me" in camera_lower or "reference to me avatar" in camera_lower:
                speaker = "wayne"
            else:
                speaker = "scene"
        elif "custom character" in header_lower or "guest" in header_lower or "ted" in header_lower:
            speaker = "guest"
        elif "using reference picture me" in camera_lower or "reference to me avatar" in camera_lower or "wayne" in header_lower:
            speaker = "wayne"
        elif "reference to guest" in camera_lower or "reference to doctor" in camera_lower:
            speaker = "guest"
        else:
            speaker = "scene" if ("scene" in header_lower or "broll" in header_lower) else "wayne"

        if script_text or camera_text:
            clips.append({
                "clip_id": clip_id,
                "title": title_text,
                "speaker": speaker,
                "script": script_text,
                "camera": camera_text
            })

    # 2. Parse B-Roll Picture Prompts
    broll_blocks = re.split(r'(?m)^#{2,4}\s+B-Roll\s+', broll_content, flags=re.IGNORECASE)
    if len(broll_blocks) > 1:
        for block in broll_blocks[1:]:
            lines = block.strip().split("\n")
            header = lines[0].strip()

            if header.startswith("Short") or header.startswith("S") or "disclaimer" in header.lower() or "000100" in header:
                continue

            id_match = re.match(r'(\d+)', header)
            b_id = id_match.group(1) if id_match else f"{len(brolls)+102}"
            title = f"B-Roll {b_id}: " + re.sub(r'^\d+[\s:\-–—]*', '', header).strip(': ')
            prompt_lines = []
            for line in lines[1:]:
                line_str = line.strip()
                if line_str.startswith("## ") or line_str.startswith("---") or line_str.startswith("```"):
                    break
                if line_str:
                    prompt_lines.append(line_str)
            prompt_text = " ".join(prompt_lines).strip(' "\'\u201c\u201d`')
            prompt_text = re.sub(r'^(?:\*\*Prompt:\*\*|####\s*Prompt:|Prompt:)\s*', '', prompt_text, flags=re.IGNORECASE).strip(' "\'\u201c\u201d`')
            if prompt_text:
                brolls.append({
                    "broll_id": b_id,
                    "title": title,
                    "prompt": prompt_text
                })
    else:
        for line in broll_content.split("\n"):
            line_s = line.strip()
            a_match = re.match(r'^[*-]?\s*[`*]*([Aa]\d+)[`*]*:\s*(.*)', line_s)
            if a_match:
                a_code = a_match.group(1).upper()
                a_prompt = a_match.group(2).strip(' "\'\u201c\u201d`')
                if a_prompt:
                    brolls.append({
                        "broll_id": a_code,
                        "title": f"B-Roll {a_code}",
                        "prompt": a_prompt
                    })
                continue

            bullet_match = re.match(r'^[*-]\s+[`*]*broll_?(\d+)[`*]*:\s*(.*)', line_s, flags=re.IGNORECASE)
            if bullet_match:
                b_num = bullet_match.group(1)
                b_prompt = bullet_match.group(2).strip(' "\'\u201c\u201d`')
                if b_prompt:
                    brolls.append({
                        "broll_id": b_num,
                        "title": f"B-Roll {b_num}: (Matches Clip {b_num})",
                        "prompt": b_prompt
                    })

    return clips, brolls, ref_assets


def generate_overlay_js_content(clips: list, brolls: list, context: str = "protocols", ref_assets: dict = None) -> str:
    """Generate complete standalone overlay.js content with Dual Mode, Aspect Presets, 5-Batch, and Swarm Orchestrator."""
    json_clips = json.dumps(clips, indent=2)
    json_brolls = json.dumps(brolls, indent=2)

    return f"""(function() {{
  // Purge any existing overlay instances
  document.querySelectorAll('#ks-floating-flow-hud, #ks-split-sidebar-root, #ks-overlay-root, .ks-hud-bar').forEach(el => el.remove());
  window.__KS_DISMISSED__ = false;

  // Handle Google Flow Trusted Types CSP
  if (window.trustedTypes && window.trustedTypes.createPolicy) {{
    try {{
      window.__KS_POLICY__ = window.__KS_POLICY__ || window.trustedTypes.defaultPolicy || window.trustedTypes.createPolicy('default', {{
        createHTML: s => s,
        createScript: s => s,
        createScriptURL: s => s
      }});
    }} catch(e) {{
      try {{
        window.__KS_POLICY__ = window.__KS_POLICY__ || window.trustedTypes.createPolicy('keystone-policy-' + Date.now(), {{
          createHTML: s => s
        }});
      }} catch(e2) {{}}
    }}
  }}

  function setSafeHTML(elem, htmlStr) {{
    if (window.__KS_POLICY__ && window.__KS_POLICY__.createHTML) {{
      elem.innerHTML = window.__KS_POLICY__.createHTML(htmlStr);
    }} else {{
      try {{
        elem.innerHTML = htmlStr;
      }} catch(e) {{
        const range = document.createRange();
        const frag = range.createContextualFragment(htmlStr);
        elem.replaceChildren(frag);
      }}
    }}
  }}

  const OVERLAY_ID = 'ks-floating-flow-hud';
  const AVATAR_SCRIPTS = {json_clips};
  const BROLL_SCRIPTS = {json_brolls};
  window.AVATAR_SCRIPTS = AVATAR_SCRIPTS;
  window.BROLL_SCRIPTS = BROLL_SCRIPTS;

  let videoIndex = parseInt(localStorage.getItem('ks_video_index') || '0', 10);
  let brollIndex = parseInt(localStorage.getItem('ks_broll_index') || '0', 10);
  if (videoIndex >= AVATAR_SCRIPTS.length) videoIndex = 0;
  if (brollIndex >= BROLL_SCRIPTS.length) brollIndex = 0;
  let activeTab = localStorage.getItem('ks_active_tab_mode') || 'video';
  let execMode = localStorage.getItem('ks_flow_exec_mode') || 'manual'; // 'manual' | 'swarm'
  let isCollapsed = localStorage.getItem('ks_hud_collapsed') === 'true';

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function setStatus(msg, col='#00f0ff') {{
    const statusEl = document.getElementById('ks-hud-status');
    if (statusEl) {{
      statusEl.innerText = msg;
      statusEl.style.color = col;
      statusEl.style.display = 'block';
    }}
  }}

  // Thoroughly clean all reference chips & prompt bar contents
  function ksCleanPromptBarAndChips() {{
    try {{
      const clearBtn = Array.from(document.querySelectorAll('button')).find(b => 
        ((b.innerText || '') + ' ' + (b.getAttribute('aria-label') || '')).toLowerCase().includes('clear prompt') &&
        !b.closest('#ks-floating-flow-hud')
      ) || Array.from(document.querySelectorAll('button')).find(b => 
        b.innerText.includes('close') && !b.closest('#ks-floating-flow-hud')
      );
      if (clearBtn) clearBtn.click();

      const chipCancels = Array.from(document.querySelectorAll('button')).filter(b => 
        b.innerText.includes('cancel') && !b.closest('#ks-floating-flow-hud')
      );
      chipCancels.forEach(b => b.click());
    }} catch(e) {{
      console.warn('[OverlayHUD] Clean prompt error:', e);
    }}
  }}

  // Direct Local ProseMirror/Slate Injector with Native Enter Submission
  function ksInjectPromptText(text, submit=true) {{
    try {{
      ksCleanPromptBarAndChips();
      const editor = document.querySelector('.ProseMirror') ||
                     document.querySelector('[data-slate-editor="true"]') || 
                     document.querySelector('[contenteditable="true"]') ||
                     document.querySelector('div.sc-36b67ffc-1 p');
      if (editor) {{
        editor.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, text);
        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
        
        if (submit) {{
          setTimeout(() => {{
            const btn = document.querySelector('button.generate-icon-button, [aria-label="Start generation"]');
            if (btn && !btn.disabled) {{
              btn.click();
              btn.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
              btn.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
              btn.dispatchEvent(new MouseEvent('click', {{ bubbles: true }}));
            }}
            window.__KEYSTONE_CDP_ENTER = Date.now();
          }}, 120);
        }}
        return true;
      }}
    }} catch(e) {{
      console.warn('[OverlayHUD] Local inject error:', e);
    }}
    return false;
  }}

  // Aspect Ratio & Quality Preset Applier
  window.ksSetPreset = async function(preset) {{
    setStatus(`⚙️ Setting ${{preset.label}}...`, '#00f0ff');
    try {{
      const resp = await fetch('http://127.0.0.1:9879/api/flow_preset', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(preset)
      }});
      const data = await resp.json();
      if (data && data.ok) {{
        setStatus(`✅ Set: ${{data.pillText || preset.label}}`, '#10b981');
      }} else {{
        setStatus(`⚠️ ${{data?.error || 'Preset failed'}}`, '#ef4444');
      }}
    }} catch(e) {{
      setStatus(`⚠️ Preset error: ${{e.message}}`, '#ef4444');
    }}
  }};

  // Live State Sync to Daemon (Port 9879)
  function syncClipState(vIdx, bIdx) {{
    localStorage.setItem('ks_video_index', vIdx.toString());
    localStorage.setItem('ks_broll_index', bIdx.toString());
    localStorage.setItem('ks_active_tab_mode', activeTab);
    localStorage.setItem('ks_flow_exec_mode', execMode);
    try {{
      const clip = AVATAR_SCRIPTS[vIdx] || {{}};
      fetch('http://127.0.0.1:9879/api/clip_state', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          clip_index: vIdx,
          clip_id: clip.clip_id || '000101',
          title: clip.title || '',
          total_clips: AVATAR_SCRIPTS.length,
          broll_index: bIdx,
          total_broll: BROLL_SCRIPTS.length,
          active_tab: activeTab,
          exec_mode: execMode
        }})
      }}).catch(() => {{}});
    }} catch(e) {{}}
  }}

  function isGuestClip(item) {{
    if (!item) return false;
    if (item.speaker === 'wayne') return false;
    if (item.speaker === 'guest') return true;
    const title = (item.title || '').toLowerCase();
    const camera = (item.camera || '').toLowerCase();
    if (camera.includes('reference to me avatar')) return false;
    if (title.includes('guest') || title.includes('custom character')) return true;
    if (camera.includes('reference to guest') || camera.includes('reference to doctor')) return true;
    return false;
  }}

  // MASTER SPEAKER INJECTION (Wayne / Guest) - WITH SUBMIT & ENTER
  window.ksExecuteSpeaker = async function(speakerType, submitNow=true) {{
    if (!AVATAR_SCRIPTS || AVATAR_SCRIPTS.length === 0) return;
    if (videoIndex >= AVATAR_SCRIPTS.length) videoIndex = 0;

    const btnWayne = document.getElementById('ks-btn-wayne');
    const btnGuest = document.getElementById('ks-btn-guest');
    const item = AVATAR_SCRIPTS[videoIndex];
    if (btnWayne) btnWayne.style.opacity = '0.6';
    if (btnGuest) btnGuest.style.opacity = '0.6';
    
    activeTab = 'video';
    const isGuest = speakerType === 'guest' || speakerType === 'ted';
    const label = isGuest ? '🎭 Guest (Char + _2)' : '👤 Wayne (Avatar + _1)';
    setStatus(`⏳ ${{label}} Submitting...`, isGuest ? '#c084fc' : '#fbbf24');

    try {{
      const resp = await fetch('http://127.0.0.1:9879/api/avatar_inject', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          speaker: isGuest ? 'guest' : 'wayne',
          cloth: isGuest ? 'cloth_2' : 'cloth_1',
          background: isGuest ? 'background_2' : 'background_1',
          script_text: item.script,
          camera_text: item.camera,
          submit: submitNow
        }})
      }});

      const res = await resp.json();
      if (res && res.ok) {{
        setStatus(`✅ ${{isGuest ? 'Guest' : 'Wayne'}} (${{videoIndex + 1}}) Submitted!`, '#10b981');
        videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }} else {{
        ksInjectPromptText(item.script, submitNow);
        setStatus(`✅ ${{isGuest ? 'Guest' : 'Wayne'}} (${{videoIndex + 1}}) Injected & Entered!`, '#10b981');
        videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }}
    }} catch(err) {{
      ksInjectPromptText(item.script, submitNow);
      setStatus(`✅ ${{isGuest ? 'Guest' : 'Wayne'}} (${{videoIndex + 1}}) Injected & Entered!`, '#10b981');
      videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
      syncClipState(videoIndex, brollIndex);
      await sleep(350);
      renderHUD();
    }} finally {{
      if (btnWayne) btnWayne.style.opacity = '1.0';
      if (btnGuest) btnGuest.style.opacity = '1.0';
    }}
  }};

  window.ksExecuteWayne = () => window.ksExecuteSpeaker('wayne', true);
  window.ksExecuteGuest = () => window.ksExecuteSpeaker('guest', true);

  // MASTER SCENE PROMPT INJECTION - WITH SUBMIT & ENTER
  window.ksExecuteScene = async function(submitNow=true) {{
    if (!AVATAR_SCRIPTS || AVATAR_SCRIPTS.length === 0) return;
    if (videoIndex >= AVATAR_SCRIPTS.length) videoIndex = 0;

    const btnScene = document.getElementById('ks-btn-scene');
    const item = AVATAR_SCRIPTS[videoIndex];
    if (btnScene) btnScene.style.opacity = '0.6';
    activeTab = 'video';
    setStatus(`⏳ 🎬 Scene (${{videoIndex + 1}}) Submitting...`, '#00f0ff');

    ksCleanPromptBarAndChips();
    const promptText = item.camera || item.script;

    try {{
      const resp = await fetch('http://127.0.0.1:9879/api/avatar_inject', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          speaker: 'scene',
          cloth: null,
          background: null,
          script_text: promptText,
          camera_text: '',
          submit: submitNow
        }})
      }});

      const res = await resp.json();
      if (res && res.ok) {{
        setStatus(`✅ Scene (${{videoIndex + 1}}) Submitted!`, '#10b981');
        videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }} else {{
        ksInjectPromptText(promptText, submitNow);
        setStatus(`✅ Scene (${{videoIndex + 1}}) Injected & Entered!`, '#10b981');
        videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }}
    }} catch(err) {{
      ksInjectPromptText(promptText, submitNow);
      setStatus(`✅ Scene (${{videoIndex + 1}}) Injected & Entered!`, '#10b981');
      videoIndex = (videoIndex + 1) % AVATAR_SCRIPTS.length;
      syncClipState(videoIndex, brollIndex);
      await sleep(350);
      renderHUD();
    }} finally {{
      if (btnScene) btnScene.style.opacity = '1.0';
    }}
  }};

  // MASTER B-ROLL PROMPT INJECTION - WITH SUBMIT & ENTER
  window.ksExecuteBRoll = async function(submitNow=true) {{
    if (!BROLL_SCRIPTS || BROLL_SCRIPTS.length === 0) return;
    if (brollIndex >= BROLL_SCRIPTS.length) brollIndex = 0;

    const btnBRoll = document.getElementById('ks-btn-broll');
    const item = BROLL_SCRIPTS[brollIndex];
    if (btnBRoll) btnBRoll.style.opacity = '0.6';
    activeTab = 'broll';
    setStatus(`⏳ B-Roll (${{brollIndex + 1}}/${{BROLL_SCRIPTS.length}}) Submitting...`, '#00f0ff');

    ksCleanPromptBarAndChips();

    try {{
      const resp = await fetch('http://127.0.0.1:9879/api/avatar_inject', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          speaker: 'broll',
          script_text: item.prompt,
          camera_text: '',
          submit: submitNow
        }})
      }});

      const res = await resp.json();
      if (res && res.ok) {{
        setStatus(`✅ B-Roll (${{brollIndex + 1}}/${{BROLL_SCRIPTS.length}}) Submitted!`, '#10b981');
        brollIndex = (brollIndex + 1) % BROLL_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }} else {{
        ksInjectPromptText(item.prompt, submitNow);
        setStatus(`✅ B-Roll (${{brollIndex + 1}}/${{BROLL_SCRIPTS.length}}) Injected & Entered!`, '#10b981');
        brollIndex = (brollIndex + 1) % BROLL_SCRIPTS.length;
        syncClipState(videoIndex, brollIndex);
        await sleep(350);
        renderHUD();
      }}
    }} catch(err) {{
      ksInjectPromptText(item.prompt, submitNow);
      setStatus(`✅ B-Roll (${{brollIndex + 1}}/${{BROLL_SCRIPTS.length}}) Injected & Entered!`, '#10b981');
      brollIndex = (brollIndex + 1) % BROLL_SCRIPTS.length;
      syncClipState(videoIndex, brollIndex);
      await sleep(350);
      renderHUD();
    }} finally {{
      if (btnBRoll) btnBRoll.style.opacity = '1.0';
    }}
  }};

  // 5-BATCH SEQUENTIAL INJECTOR (Manual & Swarm Helper)
  window.ksExecute5Batch = async function() {{
    const btn5 = document.getElementById('ks-btn-5batch');
    if (btn5) btn5.style.opacity = '0.5';
    
    for (let step = 0; step < 5; step++) {{
      const curNum = (activeTab === 'video' ? videoIndex : brollIndex) + 1;
      const total = activeTab === 'video' ? AVATAR_SCRIPTS.length : BROLL_SCRIPTS.length;
      setStatus(`⏳ [${{step + 1}}/5] Prompting ${{activeTab.toUpperCase()}} ${{curNum}}/${{total}}...`, '#fbbf24');
      
      if (activeTab === 'video') {{
        const item = AVATAR_SCRIPTS[videoIndex];
        const isGuest = isGuestClip(item);
        const isScene = item?.speaker === 'scene';
        if (isScene) {{
          await window.ksExecuteScene(true);
        }} else {{
          await window.ksExecuteSpeaker(isGuest ? 'guest' : 'wayne', true);
        }}
      }} else {{
        await window.ksExecuteBRoll(true);
      }}
      await sleep(2800);
    }}
    setStatus('✅ 5-Batch Prompts Submitted & Entered!', '#10b981');
    if (btn5) btn5.style.opacity = '1.0';
  }};

  function prevClip() {{
    activeTab = 'video';
    if (videoIndex > 0) videoIndex--;
    else videoIndex = (AVATAR_SCRIPTS.length || 1) - 1;
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function nextClip() {{
    activeTab = 'video';
    videoIndex = (videoIndex + 1) % (AVATAR_SCRIPTS.length || 1);
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function resetClip() {{
    activeTab = 'video';
    videoIndex = 0;
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function prevBRoll() {{
    activeTab = 'broll';
    if (brollIndex > 0) brollIndex--;
    else brollIndex = (BROLL_SCRIPTS.length || 1) - 1;
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function nextBRoll() {{
    activeTab = 'broll';
    brollIndex = (brollIndex + 1) % (BROLL_SCRIPTS.length || 1);
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function resetBRoll() {{
    activeTab = 'broll';
    brollIndex = 0;
    syncClipState(videoIndex, brollIndex);
    renderHUD();
  }}

  function toggleCollapse() {{
    isCollapsed = !isCollapsed;
    localStorage.setItem('ks_hud_collapsed', isCollapsed.toString());
    renderHUD();
  }}

  function makeDraggable(element, handle) {{
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    handle.onmousedown = dragMouseDown;

    function dragMouseDown(e) {{
      e = e || window.event;
      if (e.target.tagName === 'BUTTON') return;
      e.preventDefault();
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
      handle.style.cursor = 'grabbing';
    }}

    function elementDrag(e) {{
      e = e || window.event;
      e.preventDefault();
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      const newTop = Math.max(10, Math.min(window.innerHeight - 60, element.offsetTop - pos2));
      const newLeft = Math.max(10, Math.min(window.innerWidth - 180, element.offsetLeft - pos1));
      element.style.top = newTop + 'px';
      element.style.left = newLeft + 'px';
      element.style.bottom = 'auto';
      element.style.right = 'auto';
      saveHudState();
    }}

    function closeDragElement() {{
      document.onmouseup = null;
      document.onmousemove = null;
      handle.style.cursor = 'grab';
    }}
  }}

  function saveHudState() {{
    const rect = hudContainer.getBoundingClientRect();
    localStorage.setItem('ks_flow_hud_state', JSON.stringify({{
      top: rect.top,
      left: rect.left,
      width: rect.width,
      height: rect.height
    }}));
  }}

  // Build Resizable Translucent HUD Container
  let hudContainer = document.createElement('div');
  hudContainer.id = OVERLAY_ID;
  
  const savedState = localStorage.getItem('ks_flow_hud_state');
  let initTop = 75;
  let initLeft = Math.max(20, window.innerWidth - 330);
  let initWidth = 310;
  if (savedState) {{
    try {{
      const p = JSON.parse(savedState);
      if (p.top && p.left) {{ initTop = p.top; initLeft = p.left; }}
      if (p.width && p.width >= 240) {{ initWidth = p.width; }}
    }} catch (e) {{}}
  }}

  hudContainer.setAttribute('style', `
    position: fixed !important;
    top: ${{initTop}}px !important;
    left: ${{initLeft}}px !important;
    width: ${{initWidth}}px !important;
    min-width: 260px !important;
    max-width: 550px !important;
    background: rgba(10, 15, 26, 0.88) !important;
    backdrop-filter: blur(18px) saturate(190%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(190%) !important;
    border: 1.5px solid rgba(0, 240, 255, 0.45) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8), 0 0 16px rgba(0, 240, 255, 0.25) !important;
    z-index: 2147483647 !important;
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #f8fafc !important;
    overflow: hidden !important;
    resize: both !important;
    user-select: none !important;
  `);
  document.body.appendChild(hudContainer);

  new ResizeObserver(() => {{
    saveHudState();
  }}).observe(hudContainer);

  function renderHUD() {{
    const totalClips = AVATAR_SCRIPTS.length || 1;
    const totalBrolls = BROLL_SCRIPTS.length || 1;
    const currentVideoNum = videoIndex + 1;
    const currentBrollNum = brollIndex + 1;
    const batchNum = Math.floor(videoIndex / 5) + 1;
    const totalBatches = Math.ceil(totalClips / 5);

    const currentClip = AVATAR_SCRIPTS[videoIndex] || {{ clip_id: '000101', title: 'Default Clip', script: '' }};
    const currentBroll = BROLL_SCRIPTS[brollIndex] || {{ broll_id: '102', title: 'Default B-Roll', prompt: '' }};
    
    const isGuest = isGuestClip(currentClip);
    const isSceneActive = currentClip.speaker === 'scene' || (!isGuest && (currentClip.title || '').toLowerCase().includes('no photo'));
    const isWayneActive = !isGuest && !isSceneActive;
    const isGuestActive = isGuest && !isSceneActive;

    const pillStyle = (color) => `
      flex: 1;
      height: 22px;
      background: rgba(15, 23, 42, 0.65) !important;
      border: 1px solid ${{color}}66 !important;
      color: ${{color}} !important;
      border-radius: 3px !important;
      font-size: 8.5px !important;
      font-weight: 800 !important;
      cursor: pointer !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 3px !important;
      transition: all 0.15s ease !important;
    `;

    setSafeHTML(hudContainer, `
      <!-- DRAGGABLE HEADER BAR -->
      <div id="ks-hud-drag-handle" style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 7px;
        background: rgba(0, 240, 255, 0.16);
        border-bottom: 1px solid rgba(0, 240, 255, 0.25);
        cursor: grab;
      ">
        <div style="display: flex; align-items: center; gap: 5px;">
          <span style="font-size: 9.5px; color: #00f0ff; font-weight: 800; letter-spacing: 0.5px;">::: 🎬 KEYSTONE HUD</span>
          <span style="font-size: 8px; background: rgba(0, 240, 255, 0.15); color: #00f0ff; padding: 1px 4px; border-radius: 2px;">V:${{currentVideoNum}}/${{totalClips}}</span>
          <span style="font-size: 8px; background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 1px 4px; border-radius: 2px;">B:${{currentBrollNum}}/${{totalBrolls}}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 3px;">
          <button id="ks-hud-min" style="background: transparent; border: none; color: #94a3b8; font-size: 10px; cursor: pointer; padding: 0 2px;" title="Minimize/Expand">${{isCollapsed ? '➕' : '➖'}}</button>
          <button id="ks-hud-close" style="background: transparent; border: none; color: #ef4444; font-size: 10px; cursor: pointer; padding: 0 2px;" title="Close">✖</button>
        </div>
      </div>

      ${{!isCollapsed ? `
        <!-- BODY CONTENT -->
        <div style="padding: 6px; display: flex; flex-direction: column; gap: 5px;">
          
          <!-- TOP DUAL MODE SWITCH -->
          <div style="display: flex; gap: 4px; background: rgba(15, 23, 42, 0.85); padding: 3px; border-radius: 5px; border: 1px solid rgba(0, 240, 255, 0.25);">
            <button id="ks-mode-manual" style="
              flex: 1;
              height: 22px;
              background: ${{execMode === 'manual' ? 'linear-gradient(135deg, rgba(0, 240, 255, 0.45), rgba(16, 185, 129, 0.35))' : 'transparent'}};
              border: ${{execMode === 'manual' ? '1.5px solid #00f0ff' : '1px solid transparent'}};
              color: ${{execMode === 'manual' ? '#00f0ff' : '#94a3b8'}};
              border-radius: 3px;
              font-size: 9px;
              font-weight: 800;
              cursor: pointer;
            ">🎮 MANUAL COCKPIT</button>
            <button id="ks-mode-swarm" style="
              flex: 1;
              height: 22px;
              background: ${{execMode === 'swarm' ? 'linear-gradient(135deg, rgba(245, 158, 11, 0.45), rgba(239, 68, 68, 0.35))' : 'transparent'}};
              border: ${{execMode === 'swarm' ? '1.5px solid #fbbf24' : '1px solid transparent'}};
              color: ${{execMode === 'swarm' ? '#fbbf24' : '#94a3b8'}};
              border-radius: 3px;
              font-size: 9px;
              font-weight: 800;
              cursor: pointer;
            ">🤖 SWARM AUTO-PILOT</button>
          </div>

          <!-- ASPECT RATIO & QUALITY PRESETS BAR -->
          <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255,255,255,0.06); border-radius: 4px; padding: 4px; display: flex; flex-direction: column; gap: 3px;">
            <div style="font-size: 7.5px; color: #64748b; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">📐 Format &amp; Quality Presets</div>
            <!-- Video Presets -->
            <div style="display: flex; gap: 3px;">
              <button id="ks-preset-vid169" style="${{pillStyle('#fbbf24')}}" title="Video, Ingredients, Omni 1.1 Flash, 720p, 10s, x1">🎬 16:9 Long (10s 720p)</button>
              <button id="ks-preset-vid916" style="${{pillStyle('#fbbf24')}}" title="Video, Ingredients, Omni 1.1 Flash, 720p, 10s, x1">📱 9:16 Shorts (10s 720p)</button>
            </div>
            <!-- Image Presets -->
            <div style="display: flex; gap: 3px;">
              <button id="ks-preset-img169" style="${{pillStyle('#00f0ff')}}" title="Image, Ingredients, 16:9, x1">🖼️ 16:9 B-Roll</button>
              <button id="ks-preset-img11" style="${{pillStyle('#00f0ff')}}" title="Image, Ingredients, 1:1, x1">🖼️ 1:1 Square</button>
              <button id="ks-preset-img916" style="${{pillStyle('#00f0ff')}}" title="Image, Ingredients, 9:16, x1">🖼️ 9:16 Shorts</button>
            </div>
          </div>

          <!-- PERMANENT REFERENCE ASSETS BAR (CLOTHES & BACKGROUND) -->
          <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 4px; padding: 4px; display: flex; flex-direction: column; gap: 3px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 7.5px; color: #c084fc; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">👔 Reference Assets (Clothes &amp; Background)</span>
              <span style="font-size: 7px; color: #94a3b8;">Image 16:9 x1</span>
            </div>
            <div style="display: flex; gap: 3px;">
              <button type="button" id="ks-btn-gen-cloth" style="${{pillStyle('#c084fc')}}" title="Generate &amp; Auto-Rename cloth_1 reference image">👔 Gen Clothes (cloth_1)</button>
              <button type="button" id="ks-btn-gen-bg" style="${{pillStyle('#00f0ff')}}" title="Generate &amp; Auto-Rename background_1 reference image">🏙️ Gen Background (bg_1)</button>
            </div>
            <div style="display: flex; gap: 3px;">
              <button type="button" id="ks-btn-rename-cloth" style="${{pillStyle('#c084fc')}}" title="Rename existing canvas clothing tile to cloth_1">🏷️ Rename Clothes</button>
              <button type="button" id="ks-btn-rename-bg" style="${{pillStyle('#00f0ff')}}" title="Rename existing canvas background tile to background_1">🏷️ Rename Background</button>
            </div>
          </div>

          <!-- PERMANENT CANVAS MEDIA RENAMING (REVERSE GRID) -->
          <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(251, 191, 36, 0.35); border-radius: 4px; padding: 4px; display: flex; flex-direction: column; gap: 3px;">
            <div style="font-size: 7.5px; color: #fbbf24; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">🏷️ Canvas Media Renaming (Reverse Grid)</div>
            <div style="display: flex; gap: 3px;">
              <button type="button" id="ks-btn-rename-videos" style="${{pillStyle('#fbbf24')}}" title="Switch to Videos tab and rename ${{totalClips}}..1">🏷️ Rename Videos (${{totalClips}}..1)</button>
              <button type="button" id="ks-btn-rename-broll" style="${{pillStyle('#00f0ff')}}" title="Switch to Images tab and rename A${{totalBrolls}}..A1">🏷️ Rename B-Roll (A${{totalBrolls}}..A1)</button>
            </div>
          </div>

          <!-- PERMANENT DOWNLOADS & MASTER DAVINCI ASSEMBLY -->
          <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 4px; display: flex; flex-direction: column; gap: 3px;">
            <div style="font-size: 7.5px; color: #94a3b8; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">📥 Downloads &amp; Master Assembly</div>
            <div style="display: flex; gap: 3px;">
              <button type="button" id="ks-btn-download-videos" style="${{pillStyle('#fbbf24')}}" title="Download all ${{totalClips}} videos (1080p)">📥 Download Videos (${{totalClips}})</button>
              <button type="button" id="ks-btn-download-broll" style="${{pillStyle('#00f0ff')}}" title="Download all ${{totalBrolls}} B-rolls (1K)">📥 Download B-Roll (${{totalBrolls}})</button>
            </div>
            <button type="button" id="ks-btn-davinci" style="
              width: 100%; height: 24px;
              background: linear-gradient(135deg, rgba(168, 85, 247, 0.40), rgba(6, 182, 212, 0.30)) !important;
              border: 1px solid #c084fc !important; color: #e9d5ff !important;
              border-radius: 3px !important; font-size: 9px !important; font-weight: 800 !important; cursor: pointer !important;
            ">🎬 ASSEMBLE DAVINCI 2-TRACK (-18dB BGM)</button>
          </div>

          ${{execMode === 'manual' ? `
            <!-- MANUAL COCKPIT CONTROLS -->
            <div style="display: flex; gap: 3px; background: rgba(15, 23, 42, 0.6); padding: 2px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.06);">
              <button id="ks-tab-video" style="
                flex: 1;
                height: 20px;
                background: ${{activeTab === 'video' ? 'rgba(251, 191, 36, 0.25)' : 'transparent'}};
                border: ${{activeTab === 'video' ? '1px solid #fbbf24' : 'none'}};
                color: ${{activeTab === 'video' ? '#fbbf24' : '#94a3b8'}};
                border-radius: 3px;
                font-size: 9px;
                font-weight: 800;
                cursor: pointer;
              ">🎥 Video (${{currentVideoNum}}/${{totalClips}})</button>
              <button id="ks-tab-broll" style="
                flex: 1;
                height: 20px;
                background: ${{activeTab === 'broll' ? 'rgba(0, 240, 255, 0.25)' : 'transparent'}};
                border: ${{activeTab === 'broll' ? '1px solid #00f0ff' : 'none'}};
                color: ${{activeTab === 'broll' ? '#00f0ff' : '#94a3b8'}};
                border-radius: 3px;
                font-size: 9px;
                font-weight: 800;
                cursor: pointer;
              ">🖼️ B-Roll (${{currentBrollNum}}/${{totalBrolls}})</button>
            </div>

            <!-- PREVIEW CARD -->
            <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 4px 6px;">
              ${{activeTab === 'video' ? `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                  <span style="font-size: 8.5px; font-weight: 800; color: ${{isGuestActive ? '#c084fc' : '#fbbf24'}};">${{currentClip.title || ('Clip ' + currentVideoNum)}}</span>
                  <span style="font-size: 8px; color: #94a3b8; font-weight: 700;">${{currentVideoNum}}/${{totalClips}}</span>
                </div>
                <div style="font-size: 8px; color: #cbd5e1; line-height: 1.25; max-height: 28px; overflow-y: auto;">
                  "${{currentClip.script || 'No script loaded'}}"
                </div>
              ` : `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                  <span style="font-size: 8.5px; font-weight: 800; color: #00f0ff;">${{currentBroll.title || ('B-Roll ' + currentBrollNum)}}</span>
                  <span style="font-size: 8px; color: #34d399; font-weight: 700;">${{currentBrollNum}}/${{totalBrolls}}</span>
                </div>
                <div style="font-size: 8px; color: #a7f3d0; line-height: 1.25; max-height: 28px; overflow-y: auto;">
                  "${{currentBroll.prompt || 'No B-roll prompt loaded'}}"
                </div>
              `}}
            </div>

            <!-- PROMPT EXECUTION BUTTON -->
            <div style="display: flex; flex-direction: column; gap: 3px;">
              ${{activeTab === 'video' ? `
                ${{isSceneActive ? `
                  <button type="button" id="ks-btn-scene" style="
                    width: 100%; height: 27px;
                    background: linear-gradient(135deg, rgba(0, 240, 255, 0.40), rgba(16, 185, 129, 0.35)) !important;
                    border: 1.5px solid #00f0ff !important; color: #00f0ff !important;
                    border-radius: 4px !important; font-size: 10px !important; font-weight: 800 !important; cursor: pointer !important;
                    display: flex !important; align-items: center !important; justify-content: center !important; gap: 4px !important;
                    box-shadow: 0 0 10px rgba(0, 240, 255, 0.40) !important;
                  ">🎬 Inject Scene &amp; Enter (${{currentVideoNum}}/${{totalClips}}) ⚡</button>
                ` : `
                  <div style="display: flex; gap: 4px;">
                    <button type="button" id="ks-btn-wayne" style="
                      flex: 1; height: 27px;
                      background: linear-gradient(135deg, rgba(251, 191, 36, 0.45), rgba(217, 119, 6, 0.30)) !important;
                      border: 1.5px solid #fbbf24 !important; color: #fbbf24 !important;
                      border-radius: 4px !important; font-size: 10px !important; font-weight: 800 !important; cursor: pointer !important;
                      display: flex !important; align-items: center !important; justify-content: center !important; gap: 3px !important;
                      box-shadow: 0 0 10px rgba(251, 191, 36, 0.45) !important;
                    ">👤 Wayne &amp; Enter (${{currentVideoNum}}/${{totalClips}}) ⚡</button>
                    <button type="button" id="ks-btn-guest" style="
                      flex: 1; height: 27px;
                      background: linear-gradient(135deg, rgba(168, 85, 247, 0.45), rgba(6, 182, 212, 0.30)) !important;
                      border: 1.5px solid #c084fc !important; color: #e9d5ff !important;
                      border-radius: 4px !important; font-size: 10px !important; font-weight: 800 !important; cursor: pointer !important;
                      display: flex !important; align-items: center !important; justify-content: center !important; gap: 3px !important;
                      box-shadow: 0 0 10px rgba(192, 132, 252, 0.45) !important;
                    ">🎭 Guest &amp; Enter (${{currentVideoNum}}/${{totalClips}}) ⚡</button>
                  </div>
                `}}
              ` : `
                <button type="button" id="ks-btn-broll" style="
                  width: 100%; height: 27px;
                  background: linear-gradient(135deg, rgba(0, 240, 255, 0.35), rgba(16, 185, 129, 0.28)) !important;
                  border: 1.5px solid #00f0ff !important; color: #00f0ff !important;
                  border-radius: 4px !important; font-size: 10px !important; font-weight: 800 !important; cursor: pointer !important;
                  display: flex !important; align-items: center !important; justify-content: center !important; gap: 4px !important;
                  box-shadow: 0 0 10px rgba(0, 240, 255, 0.40) !important;
                ">🖼️ Inject B-Roll &amp; Enter (${{currentBrollNum}}/${{totalBrolls}}) ⚡</button>
              `}}

              <!-- 5-BATCH BUTTON -->
              <button type="button" id="ks-btn-5batch" style="
                width: 100%; height: 25px;
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.35), rgba(217, 119, 6, 0.25)) !important;
                border: 1.5px solid #f59e0b !important; color: #fef08a !important;
                border-radius: 4px !important; font-size: 9.5px !important; font-weight: 800 !important; cursor: pointer !important;
                display: flex !important; align-items: center !important; justify-content: center !important; gap: 4px !important;
              ">⚡ INJECT NEXT 5 PROMPTS &amp; ENTER</button>

              <!-- NAVIGATION ROW -->
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 3px; margin-top: 1px;">
                <button type="button" id="ks-btn-hud-prev" style="flex: 1; height: 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); color: #cbd5e1; border-radius: 3px; font-size: 8.5px; font-weight: 700; cursor: pointer;">◀ Prev</button>
                <span style="font-size: 8px; color: #94a3b8; font-family: monospace;">[${{activeTab === 'video' ? currentVideoNum : currentBrollNum}}/${{activeTab === 'video' ? totalClips : totalBrolls}}]</span>
                <button type="button" id="ks-btn-hud-next" style="flex: 1; height: 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); color: #cbd5e1; border-radius: 3px; font-size: 8.5px; font-weight: 700; cursor: pointer;">Next ▶</button>
                <button type="button" id="ks-btn-hud-reset" style="height: 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); color: #94a3b8; border-radius: 3px; font-size: 8.5px; font-weight: 600; padding: 0 4px; cursor: pointer;" title="Reset to 1">↻</button>
              </div>
            </div>
          ` : `
            <!-- SWARM AUTO-PILOT DASHBOARD -->
            <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 4px; padding: 5px; display: flex; flex-direction: column; gap: 4px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 8.5px; font-weight: 800; color: #fbbf24;">BATCH PROGRESS</span>
                <span style="font-size: 8px; color: #94a3b8;">Batch ${{batchNum}}/${{totalBatches}} (${{currentVideoNum}}/${{totalClips}} clips)</span>
              </div>
              <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
                <div style="width: ${{Math.round((videoIndex / totalClips) * 100)}}%; height: 100%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
              </div>

              <!-- SWARM ACTIONS -->
              <button type="button" id="ks-btn-run-orchestrator" style="
                width: 100%; height: 26px;
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.45), rgba(16, 185, 129, 0.35)) !important;
                border: 1.5px solid #f59e0b !important; color: #fef08a !important;
                border-radius: 4px !important; font-size: 9.5px !important; font-weight: 800 !important; cursor: pointer !important;
              ">🚀 RUN 5-BATCH SWARM ORCHESTRATOR</button>
            </div>
          `}}

          <!-- STATUS BAR -->
          <div id="ks-hud-status" style="
            font-size: 8px;
            color: #00f0ff;
            background: rgba(0, 0, 0, 0.5);
            padding: 3px 5px;
            border-radius: 3px;
            font-family: monospace;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          ">● HUD Ready (Enter submission active)</div>

        </div>
      ` : ''}}
    `);

    const handle = document.getElementById('ks-hud-drag-handle');
    if (handle) makeDraggable(hudContainer, handle);

    document.getElementById('ks-hud-min')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} toggleCollapse(); }});
    document.getElementById('ks-hud-close')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} hudContainer.remove(); }});

    // Dual Mode Switch
    document.getElementById('ks-mode-manual')?.addEventListener('click', (e) => {{
      if (e) {{ e.preventDefault(); e.stopPropagation(); }}
      execMode = 'manual';
      localStorage.setItem('ks_flow_exec_mode', 'manual');
      renderHUD();
    }});
    document.getElementById('ks-mode-swarm')?.addEventListener('click', (e) => {{
      if (e) {{ e.preventDefault(); e.stopPropagation(); }}
      execMode = 'swarm';
      localStorage.setItem('ks_flow_exec_mode', 'swarm');
      renderHUD();
    }});

    // Preset Buttons
    document.getElementById('ks-preset-vid169')?.addEventListener('click', () => {{
      window.ksSetPreset({{ label: 'Video 16:9', mode: 'video', aspect: '16:9', duration: '10s', resolution: '720p', count: 'x1', ingredients: true }});
    }});
    document.getElementById('ks-preset-vid916')?.addEventListener('click', () => {{
      window.ksSetPreset({{ label: 'Video 9:16', mode: 'video', aspect: '9:16', duration: '10s', resolution: '720p', count: 'x1', ingredients: true }});
    }});
    document.getElementById('ks-preset-img169')?.addEventListener('click', () => {{
      window.ksSetPreset({{ label: 'Image 16:9', mode: 'image', aspect: '16:9', count: 'x1', ingredients: true }});
    }});
    document.getElementById('ks-preset-img11')?.addEventListener('click', () => {{
      window.ksSetPreset({{ label: 'Image 1:1', mode: 'image', aspect: '1:1', count: 'x1', ingredients: true }});
    }});
    document.getElementById('ks-preset-img916')?.addEventListener('click', () => {{
      window.ksSetPreset({{ label: 'Image 9:16', mode: 'image', aspect: '9:16', count: 'x1', ingredients: true }});
    }});

    // Manual Tab Navigation
    document.getElementById('ks-tab-video')?.addEventListener('click', (e) => {{
      if (e) {{ e.preventDefault(); e.stopPropagation(); }}
      activeTab = 'video';
      localStorage.setItem('ks_active_tab_mode', 'video');
      renderHUD();
    }});
    document.getElementById('ks-tab-broll')?.addEventListener('click', (e) => {{
      if (e) {{ e.preventDefault(); e.stopPropagation(); }}
      activeTab = 'broll';
      localStorage.setItem('ks_active_tab_mode', 'broll');
      renderHUD();
    }});

    // Prompt Execution
    document.getElementById('ks-btn-scene')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} window.ksExecuteScene(true); }});
    document.getElementById('ks-btn-wayne')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} window.ksExecuteWayne(); }});
    document.getElementById('ks-btn-guest')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} window.ksExecuteGuest(); }});
    document.getElementById('ks-btn-broll')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} window.ksExecuteBRoll(true); }});
    document.getElementById('ks-btn-5batch')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} window.ksExecute5Batch(); }});

    document.getElementById('ks-btn-hud-prev')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} activeTab === 'video' ? prevClip() : prevBRoll(); }});
    document.getElementById('ks-btn-hud-next')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} activeTab === 'video' ? nextClip() : nextBRoll(); }});
    document.getElementById('ks-btn-hud-reset')?.addEventListener('click', (e) => {{ if (e) {{ e.preventDefault(); e.stopPropagation(); }} activeTab === 'video' ? resetClip() : resetBRoll(); }});

    // Reference Asset Buttons (Generate & Auto-Rename)
    document.getElementById('ks-btn-gen-cloth')?.addEventListener('click', async () => {{
      setStatus('🔄 Generating & Renaming cloth_1...', '#c084fc');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/generate_reference_asset', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ asset_type: 'cloth_1' }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus('✅ cloth_1 Generated & Renamed on Canvas!', '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Failed to generate cloth_1'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Ref Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-gen-bg')?.addEventListener('click', async () => {{
      setStatus('🔄 Generating & Renaming background_1...', '#00f0ff');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/generate_reference_asset', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ asset_type: 'background_1' }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus('✅ background_1 Generated & Renamed on Canvas!', '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Failed to generate background_1'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Ref Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-rename-cloth')?.addEventListener('click', async () => {{
      setStatus('🏷️ Renaming cloth_1 on canvas...', '#c084fc');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/rename_reference_asset', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ asset_type: 'cloth_1' }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus('✅ cloth_1 Renamed on Canvas!', '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Failed to rename cloth_1'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Rename Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-rename-bg')?.addEventListener('click', async () => {{
      setStatus('🏷️ Renaming background_1 on canvas...', '#00f0ff');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/rename_reference_asset', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ asset_type: 'background_1' }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus('✅ background_1 Renamed on Canvas!', '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Failed to rename background_1'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Rename Error: ' + err.message, '#ef4444');
      }}
    }});

    // Swarm Actions & Batch Execution
    document.getElementById('ks-btn-run-orchestrator')?.addEventListener('click', async () => {{
      setStatus('🚀 Starting 5-Batch Swarm Loop...', '#fbbf24');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/flow_orchestrator', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ action: 'start', context: '{context}' }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus(`✅ Swarm Orchestrator Active (PID: ${{data.pid}})`, '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Failed to launch orchestrator'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Orchestrator Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-rename-broll')?.addEventListener('click', async () => {{
      setStatus(`⏳ Renaming B-Roll (A${{totalBrolls}}..A1)...`, '#00f0ff');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/batch_rename_media', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ media_type: 'images', count: totalBrolls }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus(`✅ B-Roll Rename Dispatched (A${{totalBrolls}}..A1)`, '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Rename failed'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Rename Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-rename-videos')?.addEventListener('click', async () => {{
      setStatus(`⏳ Renaming Videos (${{totalClips}}..1)...`, '#fbbf24');
      try {{
        const resp = await fetch('http://127.0.0.1:9879/api/batch_rename_media', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ media_type: 'videos', count: totalClips }})
        }});
        const data = await resp.json();
        if (data && data.ok) {{
          setStatus(`✅ Video Rename Dispatched (${{totalClips}}..1)`, '#10b981');
        }} else {{
          setStatus('⚠️ ' + (data?.error || 'Rename failed'), '#ef4444');
        }}
      }} catch(err) {{
        setStatus('⚠️ Rename Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-download-broll')?.addEventListener('click', async () => {{
      setStatus(`⏳ Downloading B-Roll 1K (${{totalBrolls}})...`, '#00f0ff');
      try {{
        await fetch('http://127.0.0.1:9879/api/batch_download_media', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ media_type: 'images', context: '{context}', count: totalBrolls }})
        }});
        setStatus('✅ B-Roll Download Dispatched', '#10b981');
      }} catch(err) {{
        setStatus('⚠️ Download Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-download-videos')?.addEventListener('click', async () => {{
      setStatus(`⏳ Downloading Videos 1080p (${{totalClips}})...`, '#fbbf24');
      try {{
        await fetch('http://127.0.0.1:9879/api/batch_download_media', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ media_type: 'videos', context: '{context}', count: totalClips }})
        }});
        setStatus('✅ Video Download Dispatched', '#10b981');
      }} catch(err) {{
        setStatus('⚠️ Download Error: ' + err.message, '#ef4444');
      }}
    }});

    document.getElementById('ks-btn-davinci')?.addEventListener('click', async () => {{
      setStatus('⏳ Assembling DaVinci 2-Track...', '#c084fc');
      try {{
        await fetch('http://127.0.0.1:9879/api/assemble_davinci_timeline', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ video_count: totalClips, broll_count: totalBrolls, context: '{context}' }})
        }});
        setStatus('✅ DaVinci Assembly Dispatched', '#10b981');
      }} catch(err) {{
        setStatus('⚠️ DaVinci Error: ' + err.message, '#ef4444');
      }}
    }});
  }}

  renderHUD();
}})();
"""


def compile_overlay_js(clips: list, brolls: list, target_js_path: str = OVERLAY_JS_PATH, ref_assets: dict = None, context: str = "protocols") -> bool:
    """Compile new standalone overlay.js and save payload JSON."""
    new_js = generate_overlay_js_content(clips, brolls, context=context, ref_assets=ref_assets)
    os.makedirs(os.path.dirname(target_js_path), exist_ok=True)
    
    with open(target_js_path, "w", encoding="utf-8") as f:
        f.write(new_js)
        
    if ref_assets is None and os.path.exists(PAYLOAD_JSON_PATH):
        try:
            with open(PAYLOAD_JSON_PATH, "r", encoding="utf-8") as pf:
                old_payload = json.load(pf)
                ref_assets = old_payload.get("ref_assets")
        except Exception:
            pass

    payload_dict = {
        "ok": True,
        "context": context,
        "video_count": len(clips),
        "broll_count": len(brolls),
        "ref_assets": ref_assets or {},
        "clips": clips,
        "brolls": brolls
    }
    with open(PAYLOAD_JSON_PATH, "w", encoding="utf-8") as pf:
        json.dump(payload_dict, pf, indent=2)
        
    state_path = os.path.join(os.path.dirname(target_js_path), "active_state.json")
    try:
        cur_state = {
            "total_clips": len(clips),
            "total_broll": len(brolls),
            "clip_index": 0,
            "clip_id": clips[0]["clip_id"] if clips else "000101",
            "broll_index": 0,
            "timestamp": time.time()
        }
        with open(state_path, "w", encoding="utf-8") as sf:
            json.dump(cur_state, sf, indent=2)
    except Exception:
        pass
        
    print(f"[OverlayCompiler] [SUCCESS] Compiled {len(clips)} video clips and {len(brolls)} B-roll prompts into {target_js_path} (Context: {context})")
    return True


def trigger_daemon_inject():
    """Trigger chrome_overlay_daemon on Port 9879 to inject updated overlay."""
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:9879/api/inject",
            data=json.dumps({"overlayId": "google_flow", "cleanFolder": False, "fresh": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[OverlayCompiler] 🚀 CDP Injection triggered: {data}")
    except Exception as e:
        print(f"[OverlayCompiler] ⚠️ Daemon inject ping failed (is daemon running?): {e}")


def main():
    parser = argparse.ArgumentParser(description="Ingest Markdown script into Google Flow Overlay HUD.")
    parser.add_argument("--script-path", "-s", type=str, help="Path to markdown script file")
    parser.add_argument("--context", "-c", type=str, default=None, help="Context/Channel (possibilities, protocols, recomposition)")
    parser.add_argument("--inject", "-i", action="store_true", help="Trigger live CDP injection via Port 9879")
    args = parser.parse_args()

    script_path = args.script_path or find_latest_script()
    print(f"[OverlayCompiler] Ingesting script: {script_path}")
    
    parsed = parse_markdown_script(script_path)
    clips = parsed[0]
    brolls = parsed[1]
    ref_assets = parsed[2] if len(parsed) > 2 else {}
    if not clips and not brolls:
        print(f"[OverlayCompiler] ⚠️ Warning: No clips or B-rolls could be parsed from script: {script_path}")
        return 1
        
    context = args.context
    if not context:
        s_lower = script_path.lower()
        if "possibilit" in s_lower:
            context = "possibilities"
        elif "recomposit" in s_lower:
            context = "recomposition"
        else:
            context = "protocols"

    print(f"[OverlayCompiler] Parsed {len(clips)} video clips and {len(brolls)} B-roll prompts (Context: {context}).")
    compile_overlay_js(clips, brolls, ref_assets=ref_assets, context=context)
    
    if args.inject:
        trigger_daemon_inject()
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
