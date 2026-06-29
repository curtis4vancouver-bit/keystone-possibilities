"""
FIX: Re-run failed Protocols videos with trimmed tag lists.
YouTube's tag limit is ~500 chars total, not 50 tags.
"""
import sys, io, os, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

LINKS = {
    "website": "https://keystonepossibilities.ca",
    "protocols": "https://www.youtube.com/@keystoneprotocols",
    "possibilities": "https://www.youtube.com/@KeystonePossibilities",
    "oac": "https://www.youtube.com/@keystonerecomposition",
}

def protocols_footer():
    return f"""

🔬 THE PROTOCOL:
This is an academic, observational case study documenting metabolic recomposition, biological stabilization, and recovery optimization. Educational purposes only.

📊 MY STATS:
• Starting: 250 lbs → Current Progress Documented
• Protocol: Mounjaro (Tirzepatide) + BPC-157/TB-500 Wolverine Stack
• Duration: 26+ Weeks

🔗 THE KEYSTONE ECOSYSTEM:
🌐 Website: {LINKS['website']}
🏗️ Construction: {LINKS['possibilities']}
🎵 Music: {LINKS['oac']}

DISCLAIMER: This content is for educational and informational purposes only. I am not a medical professional. Always consult your healthcare provider before starting any medication or supplement protocol.

#Mounjaro #GLP1 #WolverineStack #BPC157 #BodyRecomposition #MenOver40"""

def trim_tags(tags, max_chars=480):
    """Keep tags under YouTube's character limit."""
    result = []
    total = 0
    seen = set()
    for tag in tags:
        tl = tag.lower()
        if tl in seen:
            continue
        seen.add(tl)
        # Each tag + comma separator
        if total + len(tag) + 1 > max_chars:
            break
        result.append(tag)
        total += len(tag) + 1
    return result

def update_video(video_id, new_description, tags):
    try:
        current = yt.videos().list(part="snippet,status", id=video_id).execute()
        if not current["items"]:
            print(f"  ❌ {video_id} not found")
            return False
        
        snippet = current["items"][0]["snippet"]
        full_desc = new_description + protocols_footer()
        safe_tags = trim_tags(tags)
        
        yt.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": snippet["title"],
                    "description": full_desc,
                    "tags": safe_tags,
                    "categoryId": snippet["categoryId"]
                }
            }
        ).execute()
        
        tag_chars = sum(len(t) for t in safe_tags) + len(safe_tags)
        print(f"  ✅ {snippet['title'][:55]}")
        print(f"     Tags: {len(safe_tags)} ({tag_chars} chars) | Desc: {len(full_desc)} chars")
        return True
    except Exception as e:
        print(f"  ❌ {video_id}: {e}")
        return False

# Core tags (trimmed to essentials)
CORE = [
    "keystone protocols", "mounjaro", "glp-1", "body recomposition",
    "tirzepatide", "wolverine stack", "bpc-157", "bpc 157",
    "tb-500", "peptide therapy", "mens health over 40", "metabolic health",
    "muscle preservation", "ozempic", "biohacking", "longevity"
]

WOLVERINE_EXTRA = ["bpc 157 results", "bpc 157 and tb 500", "bpc 157 review",
                    "peptide injection", "peptides for healing"]

GLP_EXTRA = ["mounjaro weight loss", "tirzepatide weight loss", 
             "glp-1 recomposition", "fitness over 40"]

FAILED_VIDEOS = {
    "DW-VXf2GXk0": {
        "desc": """Since starting tirzepatide, I've felt the best I have in years. Now I'm adding the Wolverine Stack (BPC-157 + TB-500) to push recovery and healing further.

In this 10-minute case study, I break down the clinical research behind combining GLP-1 receptor agonists with regenerative peptides — and why a 43-year-old builder is willing to bet on it.

⏱️ TIMESTAMPS:
0:00 - Why I'm Adding the Wolverine Stack
2:15 - The Science Behind BPC-157 + TB-500
5:30 - My Protocol & Dosing
8:00 - Results & What's Next""",
        "tags": CORE + WOLVERINE_EXTRA
    },
    "c--naKpO5_M": {
        "desc": """Can the Wolverine Stack actually repair a body broken down by 20+ years of construction? BPC-157 and TB-500 peptides are being called the most promising regenerative combination in clinical research.

I'm putting them to the test — live, documented, no BS.

⏱️ TIMESTAMPS:
0:00 - The Builder's Body Problem
2:00 - What BPC-157 & TB-500 Actually Do
5:00 - My Real-World Protocol
7:30 - Week-by-Week Results""",
        "tags": CORE + WOLVERINE_EXTRA
    },
    "3giPCEFfVTY": {
        "desc": """Construction is destroying my body at 43. Chronic inflammation, joint pain, and metabolic dysfunction — the reality of building luxury homes with your hands for two decades.

This is my documented case study using the Wolverine Stack (BPC-157 + TB-500) alongside GLP-1 therapy to attempt a full biological rebuild.

⏱️ TIMESTAMPS:
0:00 - The Physical Cost of Construction
2:30 - Why Traditional Recovery Fails
5:00 - The Wolverine Stack Protocol
8:00 - Measurable Changes""",
        "tags": CORE + WOLVERINE_EXTRA
    },
    "NLTSFHhT9cc": {
        "desc": """The Wolverine Stack — can BPC-157 and TB-500 actually fix a 43-year-old builder? Full case study with clinical evidence, real dosing protocols, and documented results.

No hype. No affiliate links. Just a builder testing regenerative peptides on camera and reporting what happens.

⏱️ TIMESTAMPS:
0:00 - Introduction & Background
2:00 - Clinical Evidence Review
5:00 - My Exact Protocol
8:00 - Results & Takeaways""",
        "tags": CORE + WOLVERINE_EXTRA
    },
    "zFUwRvTI7EU": {
        "desc": """The Wolverine Stack: BPC-157 + TB-500 — the full case study from a 43-year-old general contractor. Documenting everything from dosing to results with clinical research citations.

This is the Builder Blueprint approach to peptide therapy: evidence-based, methodically documented, and brutally honest.

⏱️ TIMESTAMPS:
0:00 - What Is the Wolverine Stack?
2:30 - The Science of BPC-157 & TB-500
5:30 - Protocol & Dosing Breakdown
8:30 - Key Findings""",
        "tags": CORE + WOLVERINE_EXTRA
    },
    "pBB4W2kOgQM": {
        "desc": """45 lbs lost. Zero muscle lost. This is what body recomposition actually looks like on GLP-1 therapy (Mounjaro/Tirzepatide) when you protect the muscle.

Most people losing weight on GLP-1 lose 30-40% muscle mass. I lost NONE. Here's the full protocol breakdown.

⏱️ TIMESTAMPS:
0:00 - The 45 lb Transformation
2:00 - Why Most GLP-1 Users Lose Muscle
4:30 - My Muscle Protection Protocol
7:00 - Results""",
        "tags": CORE + GLP_EXTRA
    },
    "ynSo4eOaIeU": {
        "desc": """I lost 38 lbs on Mounjaro — while building houses full-time. 26 weeks of tirzepatide documented from start to finish.

Most GLP-1 content comes from people sitting at desks. This is what happens when you run a GLP-1 protocol while doing physically demanding construction work every day.

⏱️ TIMESTAMPS:
0:00 - The Construction + GLP-1 Experiment
2:30 - Weekly Dosing & Adjustments
5:00 - Physical Performance Changes
8:00 - Final Results & What's Next""",
        "tags": CORE + GLP_EXTRA
    },
}

print("=" * 70)
print("  RE-RUNNING FAILED PROTOCOLS UPDATES (trimmed tags)")
print("=" * 70)

ok = 0
fail = 0
for vid_id, data in FAILED_VIDEOS.items():
    r = update_video(vid_id, data["desc"], data["tags"])
    ok += 1 if r else 0
    fail += 0 if r else 1
    time.sleep(1)

print(f"\n  Results: {ok} updated, {fail} failed")
print("=" * 70)
