"""
MASTER UPDATE SCRIPT — Keystone YouTube Empire
Updates descriptions, tags, and hashtags for ALL Protocols and Possibilities videos.
Uses verified links and competitor intelligence tags.
"""
import sys, io, os, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

# ============================================================
# VERIFIED LINKS (from verification step)
# ============================================================
LINKS = {
    "website": "https://keystonepossibilities.ca",
    "protocols": "https://www.youtube.com/@keystoneprotocols",
    "possibilities": "https://www.youtube.com/@KeystonePossibilities",  # Will update when handle changes
    "oac": "https://www.youtube.com/@keystonerecomposition",
}

# ============================================================
# CHANNEL IDS
# ============================================================
PROTOCOLS_ID = "UCxURlqMNhAtxUTpdXmlOYaw"
POSSIBILITIES_ID = "UCu8gdU_R8XE2RvcttGa3drg"

# ============================================================
# MASTER TAG LISTS (from competitor intelligence)
# ============================================================
PROTOCOLS_CORE_TAGS = [
    "keystone protocols", "mounjaro", "glp-1", "glp1", "body recomposition",
    "tirzepatide", "mounjaro weight loss", "wolverine stack", "bpc-157", "bpc 157",
    "tb-500", "peptide therapy", "mens health over 40", "metabolic health",
    "weight loss men", "muscle preservation", "ozempic", "semaglutide",
    "peptide protocols", "biohacking", "longevity"
]

PROTOCOLS_ROTATING_TAGS = {
    "wolverine": ["bpc 157 results", "bpc 157 and tb 500", "bpc 157 review", 
                   "bpc 157 dosing", "bpc 157 benefits", "does bpc 157 work",
                   "wolverine stack peptides", "peptide injection", "peptides for healing",
                   "peptides explained", "bpc 157 peptide"],
    "glp1": ["mounjaro canada", "mounjaro cost canada", "ozempic vs mounjaro",
             "mounjaro side effects", "tirzepatide weight loss", "glp-1 recomposition",
             "retatrutide", "glp 1 muscle loss"],
    "body": ["body recomposition over 40", "muscle retention glp-1", "cold plunge benefits",
             "reverse aging", "peter attia", "metabolic health men", "fitness over 40"],
}

POSSIBILITIES_TAGS = [
    "keystone possibilities", "luxury construction", "project management",
    "custom homes vancouver", "north vancouver contractor", "west vancouver renovation",
    "luxury renovation", "general contractor vancouver", "custom home build",
    "construction management", "home renovation", "vancouver real estate",
    "north shore construction", "bc construction", "luxury home builder"
]

# ============================================================
# DESCRIPTION TEMPLATES
# ============================================================
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


def possibilities_footer():
    return f"""

🏗️ KEYSTONE POSSIBILITIES LTD.
General Contractor | North & West Vancouver
Custom Homes • Luxury Renovations • Project Management

📋 SERVICES:
• Full-scope project management
• Custom home builds & luxury renovations
• Pre-construction consulting
• Site supervision & quality control

🔗 THE KEYSTONE ECOSYSTEM:
🌐 Website: {LINKS['website']}
💪 Health: {LINKS['protocols']}
🎵 Music: {LINKS['oac']}

#LuxuryConstruction #ProjectManagement #CustomHomes #Vancouver #NorthVancouver"""


# ============================================================
# PROTOCOLS VIDEO-SPECIFIC DESCRIPTIONS
# ============================================================
PROTOCOLS_DESCRIPTIONS = {
    "DW-VXf2GXk0": {
        "desc": """Since starting tirzepatide, I've felt the best I have in years. Now I'm adding the Wolverine Stack (BPC-157 + TB-500) to push recovery and healing further.

In this 10-minute case study, I break down the clinical research behind combining GLP-1 receptor agonists with regenerative peptides — and why a 43-year-old builder is willing to bet on it.

⏱️ TIMESTAMPS:
0:00 - Why I'm Adding the Wolverine Stack
2:15 - The Science Behind BPC-157 + TB-500
5:30 - My Protocol & Dosing
8:00 - Results & What's Next""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["wolverine"]
    },
    "c--naKpO5_M": {
        "desc": """Can the Wolverine Stack actually repair a body that's been broken down by 20+ years of construction? BPC-157 and TB-500 peptides are being called the most promising regenerative combination in clinical research.

I'm putting them to the test — live, documented, no BS. This is what happens when a builder treats his body like a jobsite that needs structural repair.

⏱️ TIMESTAMPS:
0:00 - The Builder's Body Problem
2:00 - What BPC-157 & TB-500 Actually Do
5:00 - My Real-World Protocol
7:30 - Week-by-Week Results""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["wolverine"]
    },
    "3giPCEFfVTY": {
        "desc": """Construction is destroying my body at 43. Chronic inflammation, joint pain, and metabolic dysfunction — the reality of building luxury homes with your hands for two decades.

This is my documented case study using the Wolverine Stack (BPC-157 + TB-500) alongside GLP-1 therapy to attempt a full biological rebuild.

⏱️ TIMESTAMPS:
0:00 - The Physical Cost of Construction
2:30 - Why Traditional Recovery Fails
5:00 - The Wolverine Stack Protocol
8:00 - Measurable Changes""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["wolverine"] + ["construction worker health", "joint pain recovery"]
    },
    "NLTSFHhT9cc": {
        "desc": """The Wolverine Stack — can BPC-157 and TB-500 actually fix a 43-year-old builder? This is the full case study with clinical evidence, real dosing protocols, and documented results.

No hype. No affiliate links. Just a builder testing regenerative peptides on camera and reporting what happens.

⏱️ TIMESTAMPS:
0:00 - Introduction & Background
2:00 - Clinical Evidence Review
5:00 - My Exact Protocol
8:00 - Results & Takeaways""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["wolverine"]
    },
    "zFUwRvTI7EU": {
        "desc": """The Wolverine Stack: BPC-157 + TB-500 — the full case study from a 43-year-old general contractor. Documenting everything from dosing to results with clinical research citations.

This is the Builder Blueprint approach to peptide therapy: evidence-based, methodically documented, and brutally honest.

⏱️ TIMESTAMPS:
0:00 - What Is the Wolverine Stack?
2:30 - The Science of BPC-157 & TB-500
5:30 - Protocol & Dosing Breakdown
8:30 - Key Findings""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["wolverine"]
    },
    "pBB4W2kOgQM": {
        "desc": """45 lbs lost. Zero muscle lost. This is what body recomposition actually looks like on GLP-1 therapy (Mounjaro/Tirzepatide) when you protect the muscle.

Most people losing weight on GLP-1 lose 30-40% muscle mass. I lost NONE. Here's exactly how — the full protocol breakdown.

⏱️ TIMESTAMPS:
0:00 - The 45 lb Transformation
2:00 - Why Most GLP-1 Users Lose Muscle
4:30 - My Muscle Protection Protocol
7:00 - DEXA Scan Results""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["glp1"] + PROTOCOLS_ROTATING_TAGS["body"]
    },
    "PwQqt6U0kdo": {
        "desc": """Losing muscle on GLP-1? You're not alone — studies show 30-40% of weight loss on semaglutide and tirzepatide comes from lean mass. But it doesn't have to be that way.

Here's exactly how I preserved every pound of muscle through 26+ weeks of Mounjaro — while working full-time in construction.

⏱️ TIMESTAMPS:
0:00 - The GLP-1 Muscle Loss Crisis
2:00 - The Science of Lean Mass Preservation
5:00 - My Exact Nutrition & Training Protocol
8:00 - Before/After Results""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["glp1"]
    },
    "d9wBAZgZx7E": {
        "desc": """How I lost 38 lbs on Mounjaro (Tirzepatide) at 42 years old — while running a construction company and building luxury homes in North Vancouver.

This isn't a weight loss vlog. This is a structured metabolic case study documenting the real effects of GLP-1 receptor agonist therapy on a working tradesman's body.

⏱️ TIMESTAMPS:
0:00 - Starting Point: 250 lbs
2:00 - Why I Chose Tirzepatide
4:30 - Weekly Protocol & Side Effects
7:00 - The 38 lb Result""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["glp1"]
    },
    "ynSo4eOaIeU": {
        "desc": """I lost 38 lbs on Mounjaro — while building houses full-time. 26 weeks of tirzepatide documented from start to finish.

Most GLP-1 content comes from people sitting at desks. This is what happens when you run a GLP-1 protocol while doing physically demanding construction work every day.

⏱️ TIMESTAMPS:
0:00 - The Construction + GLP-1 Experiment
2:30 - Weekly Dosing & Adjustments
5:00 - Physical Performance Changes
8:00 - Final Results & What's Next""",
        "extra_tags": PROTOCOLS_ROTATING_TAGS["glp1"] + ["construction worker", "physical labor weight loss"]
    },
}

# ============================================================
# POSSIBILITIES VIDEO DESCRIPTIONS
# ============================================================
POSSIBILITIES_DESCRIPTIONS = {
    "IhgwE96Jcs4": {
        "desc": """Your luxury build is failing — and you probably don't even know it yet. As a general contractor in North & West Vancouver, I've seen million-dollar projects go sideways because of one missing piece: proper project management.

In this video, I break down the 3 critical failure points that destroy luxury builds and how to prevent them before your investment goes up in smoke.""",
    },
    "WgnbFGenZC8": {
        "desc": """Why does every luxury build in Vancouver fail without a dedicated project manager? Because the complexity of a custom home build in North Vancouver requires someone whose only job is quality control, timeline management, and contractor coordination.

I've managed projects across the North Shore — here's what happens when you try to skip the PM.""",
    },
    "WGlZeW3Lz9M": {
        "desc": """Go inside a real North Vancouver custom home build — from foundation pour to structural framing. This is what professional construction management looks like on the ground.

Keystone Possibilities Ltd. provides full-scope project management for luxury custom homes and renovations in North & West Vancouver.""",
    },
}

# ============================================================
# EXECUTE UPDATES
# ============================================================
def update_video(video_id, new_description, extra_tags=None, is_protocols=True):
    """Update a single video's description and tags."""
    try:
        # Get current video data
        current = yt.videos().list(part="snippet,status", id=video_id).execute()
        if not current["items"]:
            print(f"  ❌ Video {video_id} not found")
            return False
        
        video = current["items"][0]
        snippet = video["snippet"]
        
        # Build new tags
        if is_protocols:
            base_tags = PROTOCOLS_CORE_TAGS.copy()
        else:
            base_tags = POSSIBILITIES_TAGS.copy()
        
        if extra_tags:
            base_tags.extend(extra_tags)
        
        # Deduplicate tags while preserving order
        seen = set()
        unique_tags = []
        for tag in base_tags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_tags.append(tag)
        
        # Add footer to description
        if is_protocols:
            full_description = new_description + protocols_footer()
        else:
            full_description = new_description + possibilities_footer()
        
        # Update
        yt.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": snippet["title"],
                    "description": full_description,
                    "tags": unique_tags[:50],  # YouTube max is ~500 chars total
                    "categoryId": snippet["categoryId"]
                }
            }
        ).execute()
        
        print(f"  ✅ Updated: {snippet['title'][:55]}")
        print(f"     Tags: {len(unique_tags)} | Desc length: {len(full_description)} chars")
        return True
        
    except Exception as e:
        print(f"  ❌ FAILED {video_id}: {e}")
        return False


# ============================================================
# RUN IT
# ============================================================
print("=" * 70)
print("  EXECUTING MASTER UPDATE — KEYSTONE PROTOCOLS (9 videos)")
print("=" * 70)

success_count = 0
fail_count = 0

for video_id, data in PROTOCOLS_DESCRIPTIONS.items():
    result = update_video(
        video_id, 
        data["desc"], 
        extra_tags=data.get("extra_tags", []),
        is_protocols=True
    )
    if result:
        success_count += 1
    else:
        fail_count += 1
    time.sleep(1)  # Rate limit protection

print(f"\n  Protocols: {success_count} updated, {fail_count} failed")

print("\n" + "=" * 70)
print("  EXECUTING MASTER UPDATE — KEYSTONE POSSIBILITIES (3 construction videos)")
print("  (Skipping CScmP8MYaWE — health video on wrong channel)")
print("=" * 70)

for video_id, data in POSSIBILITIES_DESCRIPTIONS.items():
    result = update_video(
        video_id, 
        data["desc"],
        is_protocols=False
    )
    if result:
        success_count += 1
    else:
        fail_count += 1
    time.sleep(1)

print(f"\n  TOTAL: {success_count} updated, {fail_count} failed")
print("\n" + "=" * 70)
print("  UPDATE COMPLETE")
print("=" * 70)
