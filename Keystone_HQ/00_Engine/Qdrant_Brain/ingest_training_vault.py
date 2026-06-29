"""
Ingest the Keystone Agent Training & Continuity Vault into the brain.
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5")

TRAINING_VAULT_DOC = """
KEYSTONE AGENT TRAINING & CONTINUITY VAULT
This document serves as the live training corpus and context database for the Google Antigravity agentic workflow. It bridges the Gap between local vector databases and Google Workspace documents, maintaining strict continuity across video production, brand compliance, and competitive research.

1. YOUTUBE VIDEO CONTINUITY LOG
Last Released Video (Baseline):
Format: Spoken metabolic breakdown + Melodic House visualizer.
Narrative Anchor: "Phase 2" hypertrophy build. Transitioning away from depletive weight loss to structural, load-bearing muscle preservation.
Visual Assets: Squamish great room Great views, cold plunge, heavy lifting B-roll.
Audio Base: Steady pulse Melodic House (124 BPM).

Next Planned Video (Active Context):
Target Title: The Depletive Metabotype (Why 34% of GLP-1 weight loss is structural muscle).
Narrative Arc: Framing muscle loss as "structural damage" and "planning theater."
Visual Prompts (Veo 3.1): High-performance mountain architecture matching Squamish grade variations, contrasting with clinical weight training clips.
Solfeggio/Music Signal: Melodic House, Deep Cello, Soulful Female Vocals.

2. COMPLIANCE & SCIENCE TRAINING FEED (YMYL / GLP-1 / PEPTIDES)
Grounding text to bypass YouTube's 2026 YMYL manual review filters using the EDSA Exception.
Non-Negotiable Medical Disclaimer:
"I am a residential builder, not a medical doctor. This video represents a single-subject case study (N-of-1) tracking my own metabolic administration cadence, body recomposition progress, and structural rebuild. None of this content constitutes medical advice or titration prescribing. Always consult a licensed clinical specialist."
Peer-Reviewed Academic Grounding (The "Shield" Context):
Muscle Wastage Ratio: Batsis et al. 2026 documented that up to 34.9% of total weight lost on Tier 1 GLP-1 receptor agonists is lean skeletal muscle, not fat.
Post-Titration Regain Plateau: Lin et al. 2026 proved a 75.6% weight regain plateau when stopping GLP-1s without heavy eccentric resistance training and structural metabolic stabilization.
Peptide Mechanics: Strictly frame BPC-157 and TB-500 as "In Vitro collagen synthesis research" and "cellular wound-healing mechanisms," never as injectable products for self-administration.

3. MUSIC BRAND SIGNALING (SONIC UNIVERSE)
Siloed data to keep streaming algorithms focused on pure Melodic Techno / Deep House listeners, avoiding GLP-1 crossover.
Primary Distributor: TooLost
Metadata Registry: MusicBrainz & Musixmatch (for lyrics sync)
Genre Signaling Profile:
BPM Target: 124 BPM
Sonic Elements: Deep warm cello, atmospheric pads, steady bass pulse, motivational female vocals.
Web3 Integration: On-chain UA loop (YGG partnership).

4. PROJECT MANAGEMENT & BRAND BUILDING
Grounding context for high-ticket construction pitches and local development consulting.
2026 Coastal BC High-End Design Trends (Competitor Defeat Angles):
Subterranean Luxury: Turning West Vancouver custom basements into primary wellness/recovery suites, cold plunges, and climate-controlled wine cellars opening to lower-tier gardens.
Quiet Tech: Invisible, flush-mounted smart technology. Absolutely zero wall clutter or panel wires.
The Zoned "Closed-Concept" Kitchen: Moving away from standard open-concept spaces to minimalist, slab-door architectural kitchens with concealed appliances.
Biophilic Materials: local raw cedar, local basalt stone, and glass-walled internal courtyards.
"""

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Protocol Namespace
protocol_chunks = chunk_text(TRAINING_VAULT_DOC.split("3. MUSIC BRAND SIGNALING")[0])
p_meta = [{"source": "Keystone_Agent_Training_Vault.gdoc", "section": "youtube_and_compliance"} for _ in protocol_chunks]
client.add(collection_name="protocol", documents=protocol_chunks, metadata=p_meta)
print(f"Ingested {len(protocol_chunks)} chunks into 'protocol' namespace.")

# Music Namespace
music_content = TRAINING_VAULT_DOC.split("3. MUSIC BRAND SIGNALING")[1].split("4. PROJECT MANAGEMENT")[0]
m_chunks = chunk_text(music_content)
m_meta = [{"source": "Keystone_Agent_Training_Vault.gdoc", "section": "music_signaling"} for _ in m_chunks]
# Ensure music namespace exists
if not client.collection_exists("music"):
    client.create_collection(collection_name="music", vectors_config=client.get_fastembed_vector_params())
client.add(collection_name="music", documents=m_chunks, metadata=m_meta)
print(f"Ingested {len(m_chunks)} chunks into 'music' namespace.")

# Possibilities Namespace
possibilities_content = TRAINING_VAULT_DOC.split("4. PROJECT MANAGEMENT")[1]
pos_chunks = chunk_text(possibilities_content)
pos_meta = [{"source": "Keystone_Agent_Training_Vault.gdoc", "section": "project_management_trends"} for _ in pos_chunks]
client.add(collection_name="possibilities", documents=pos_chunks, metadata=pos_meta)
print(f"Ingested {len(pos_chunks)} chunks into 'possibilities' namespace.")
