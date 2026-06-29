import json, os

path = r'c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\correction_journal.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# The corruption starts at line 262 (0-indexed 261)
# Take the first 258 lines which are valid (up through CJ-20260607-215233 closing)
# Line 258 (0-indexed 257) is the closing "}" of the last good entry

# Find the line that closes CJ-20260607-215233
good_lines = []
for i, line in enumerate(lines):
    good_lines.append(line)
    stripped = line.strip()
    if '"fingerprint": "writing scripts with personal experience' in line:
        # Next line is the closing brace of this entry
        good_lines.append(lines[i+1])  # the "}" line
        break

# Now build the rest manually
tail = """                    ,
                    {
                        "id": "CJ-20260609-172347",
                        "timestamp": "2026-06-09T17:23:47",
                        "fix": "STOP repeating stale audit results. Must VERIFY live state before reporting anything as missing.",
                        "error_type": "stale_data_repetition_and_brand_confusion",
                        "description": "Agent repeated stale SEO audit findings without re-verifying live state.",
                        "root_cause": "Agent relied on stale audit artifact instead of performing fresh verification.",
                        "prevention": "NEVER report website status from memory or old audits. ALWAYS do a FRESH Brave search or live check.",
                        "fingerprint": "reporting site status OR claiming something is missing OR SEO audit"
                    },
                    {
                        "id": "CJ-20260609-215000",
                        "timestamp": "2026-06-09T21:50:00",
                        "fix": "ABSOLUTE BAN: Never launch Chrome via Start-Process, subprocess, or any spawn command. ONLY use chrome-devtools-mcp on port 9222.",
                        "error_type": "chrome_profile_destruction",
                        "description": "Agent launched Chrome with isolated automation profile, wiping all saved passwords and sessions.",
                        "root_cause": "Agent spawned new Chrome process instead of connecting via chrome-devtools-mcp port 9222.",
                        "prevention": "NEVER launch Chrome. ONLY use chrome-devtools-mcp on port 9222. If Chrome not running, ASK WAYNE to open it. ZERO TOLERANCE.",
                        "fingerprint": "launching chrome OR Start-Process chrome OR spawning browser OR new chrome profile"
                    }
                ]
}
"""

with open(path, 'w', encoding='utf-8') as f:
    for line in good_lines:
        f.write(line)
    f.write(tail)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"SUCCESS: Valid JSON with {len(data['entries'])} entries")
print(f"Last entry: {data['entries'][-1]['id']}")
