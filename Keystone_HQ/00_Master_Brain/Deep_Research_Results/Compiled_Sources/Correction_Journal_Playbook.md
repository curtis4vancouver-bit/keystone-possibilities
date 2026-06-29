# Keystone Correction Journal & Prevention Playbook
*Compiled on 2026-06-24 - Total entries: 13*

## Entry 1: [general] - 2026-06-16T01:23:00-07:00
### 🛑 Error / Bug:
Failed to verify YouTube upload compliance requirements (missing medical disclaimers, AI disclosure, hashtag placement, and 500-char tags list) before presenting script. Also hallucinated personal protocol (CJC+GHK) instead of using verified actual protocol (GHK+BPC-157).

### 🛠️ Fix Applied:
Rewrote script to use factually accurate protocol and appended the exact YouTube metadata block required by upload_quality_gate/SKILL.md.

### 🛡️ Prevention Rule:
Never invent or hallucinate Wayne's medical/health protocols. Always verify against Research_Archives or his explicit past instructions. Always append the full YouTube metadata block (with disclaimers and AI disclosures) to every script output for copy/pasting.

---

## Entry 2: [general] - 2026-06-16T13:26:00-07:00
### 🛑 Error / Bug:
Presented scripts missing Facebook metadata, Instagram metadata, AI Twin disclosure, and 500-char tags. Had to be corrected 4 times in one session. Each correction costs Wayne real money in wasted API credits and generation time.

### 🛠️ Fix Applied:
Created a mandatory 6-section checklist: Script, B-Roll, Thumbnail, YouTube Metadata (title/desc/disclaimer/AI disclosure/hashtags/tags), Facebook Metadata, Instagram Metadata. All 6 sections MUST be present before presenting any script.

### 🛡️ Prevention Rule:
Every short script deliverable MUST include all 6 metadata sections. Run the checklist mentally before finalizing. Cross-reference upload_quality_gate/SKILL.md and the new mandatory_short_production_checklist stored in the content_pipeline brain namespace.

---

## Entry 3: [general] - 2026-06-16T00:47:00-07:00
### 🛑 Error / Bug:
Failed to double-check visual changes via screenshot before confirming to Wayne that work was done. Video sizing, logo sizing, and layout issues were reported by Wayne multiple times.

### 🛠️ Fix Applied:
Established a hard rule: Always take a screenshot and verify visual output before confirming any UI/web change is complete.

### 🛡️ Prevention Rule:
ALWAYS pull a live screenshot via chrome-devtools-mcp take_screenshot after deploying any visual change. Never tell Wayne it is done until the screenshot confirms it matches his instructions.

---

## Entry 4: [general] - 2026-06-17T18:05:53.716290
### 🛑 Error / Bug:
AI bots not whitelisted in robots.txt and missing local citations in schema

### 🛠️ Fix Applied:
Injected a robots_txt WordPress filter into functions.php to explicitly allow AI bots, and added 7 directory citations into the sameAs array.

### 🛡️ Prevention Rule:
Always explicitly allow AI crawlers (GPTBot, ClaudeBot, etc) in robots.txt via functions.php on any new WP deployment.

---

## Entry 5: [general] - 2026-06-18T04:46:30Z
### 🛑 Error / Bug:
Upscaled 1080p files sometimes return 404 from storage causing missing files

### 🛠️ Fix Applied:
Implemented a 720p fallback check. If the upsampled download returns a 404 error, strip the '_upsampled' suffix from the API request URL to fetch the raw 720p version, ensuring all generated clips are successfully captured.

### 🛡️ Prevention Rule:
Always implement a 720p fallback (without '_upsampled' suffix) to ensure all generated media is captured if upscaling fails.

---

## Entry 6: [general] - 2026-06-18T05:11:00Z
### 🛑 Error / Bug:
Dynamic session tokens caused the voice bridge to communicate with stale chat frames

### 🛠️ Fix Applied:
Implemented automatic update of voice_bridge_config.json on workspace bootstrap via scripts/update_voice_config.py using environment parameters.

### 🛡️ Prevention Rule:
Update the voice bridge configuration using update_voice_config.py during the master bootstrap routine.

---

## Entry 7: [general] - 2026-06-18T05:11:00Z
### 🛑 Error / Bug:
Setting low brightness values via DDC/CI glitches monitor firmware, enabling hardware OSD crosshair

### 🛠️ Fix Applied:
Advised the user to toggle off the hardware-level crosshair using the monitor's physical joystick OSD control menu, and documented the limitation.

### 🛡️ Prevention Rule:
Avoid values lower than 5% and inform the user that any hardware-level OSD side effects must be turned off using the physical screen buttons.

---

## Entry 8: [general] - 2026-06-18T14:48:35.642802
### 🛑 Error / Bug:
Voice Bridge double glitch on new chats

### 🛠️ Fix Applied:
Modified voice_bridge.py to dynamically get_latest_conversation_id() and removed bridge.deactivate() from session_monitor

### 🛡️ Prevention Rule:
N/A

---

## Entry 9: [general] - 2026-06-22T06:17:00.000000
### 🛑 Error / Bug:
Playwright CDP connection hangs or fails when Chrome DevTools MCP is holding port 9222 connection

### 🛠️ Fix Applied:
Decoupled the download workflow: execute asynchronous context menu clicks directly inside Chrome via evaluate_script JS tool, and run a local python daemon to fuzzy match, rename, and move downloaded files by prompt text

### 🛡️ Prevention Rule:
N/A

---

## Entry 10: [general] - 2026-06-23T15:25:00.000000
### 🛑 Error / Bug:
Connecting to Electron DevTools active port WebSocket using 'localhost' causes socket timeouts on Windows

### 🛠️ Fix Applied:
Replaced 'localhost' with '127.0.0.1' in the WebSocket URL before connecting to prevent Windows IPv6 DNS resolution issues

### 🛡️ Prevention Rule:
N/A

---

## Entry 11: [general] - 2026-06-23T08:44:04.239276
### 🛑 Error / Bug:
[orchestration] DaVinci Resolve UI was hidden behind the Chrome browser window, causing clicks to hit the wrong screen coordinate

### 🛠️ Fix Applied:
ALWAYS bring DaVinci Resolve to the foreground before performing any UI automation or click actions

### 🛡️ Prevention Rule:
ALWAYS bring DaVinci Resolve to the foreground before performing any UI automation or click actions

---

## Entry 12: [general] - 2026-06-23T08:44:25.812624
### 🛑 Error / Bug:
[orchestration] DaVinci Resolve UI was hidden behind the Chrome browser window, causing clicks to hit the wrong screen coordinate

### 🛠️ Fix Applied:
ALWAYS bring DaVinci Resolve to the foreground before performing any UI automation or click actions

### 🛡️ Prevention Rule:
ALWAYS bring DaVinci Resolve to the foreground before performing any UI automation or click actions

---

## Entry 13: [general] - 2026-06-23T08:54:21.926693
### 🛑 Error / Bug:
[backend] Action did not achieve the desired outcome or required adjustments.

### 🛠️ Fix Applied:
ok go do it

### 🛡️ Prevention Rule:
ok go do it

---

