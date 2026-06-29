"""
Ingest the Keystone Empire Master Strategy Manual into the Main brain.
This is the master document — goes into 'master' namespace so Chronos
and all orchestrator-level agents can reference it.
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5")

MASTER_DOC = """
KEYSTONE EMPIRE: MASTER STRATEGY MANUAL (MAY 2026)

SECTION 1: WEB ARCHITECTURE & PROGRAMMATIC SEO SITEMAP (keystonepossibilities.ca)
To capture high-ticket project management leads ($1.5M+ custom builds) in target geographic corridors (West Vancouver, North Vancouver, and the Sea-to-Sky corridor), deploy a programmatic SEO sitemap focusing on municipal pain points such as permit delays and sewer capacity limits, positioning Wayne as the ultimate risk-mitigator.

Core Site Directory Structure:
keystonepossibilities.ca/
- index.html: High-end Charcoal/Gold Luxury PM landing page
- sitemap.xml: XML index for search crawler submission
- robots.txt: Search engine directives, gated from AI scrapers
- project-management/west-vancouver.html: Programmatic SEO West Van
- project-management/north-vancouver.html: Programmatic SEO North Van
- project-management/squamish-corridor.html: Programmatic SEO Squamish
- design-portfolio/subterranean-luxury.html: Walk-out basements, wine cellars, recovery suites
- design-portfolio/quiet-tech-integration.html: Invisible automation, flush-mount ecosystems
- design-portfolio/biophilic-architecture.html: Raw cedar, local stone, internal courtyards
- contact/: Next.js/Supabase Lead Form

Programmatic SEO Landing Page Template:
West Vancouver Page: Targets subsurface sewer capacity (92% limits) and environmental zoning on the North Shore slope.
Squamish Page: Targets the 13-month municipal permit delay ("Planning Theater") and wind/snow loads.

SECTION 2: HIGH-TICKET PM LANDING PAGE COPY (CONVERSION ENGINE)
Dark-mode interface: Charcoal backgrounds, Matte Gold accent lines, Clean Inter typography.
Headline: ELIMINATE PLANNING THEATER. BUILD WITH PRECISION.
Subhead: From Site Clearance to final occupancy. We manage multi-million dollar residential developments in West Vancouver and the Sea-to-Sky corridor.
The Problem: The 13-Month Bottleneck. Average Squamish development permit takes 13 months. West Vancouver subsurface utility hookups at peak capacity.
Solution 1: Unified PWA Site Telemetry — proprietary Progress Web App (PWA) Command Center. Sequential Trade Logic prevents overlapping trade conflicts. Real-time progress tracking via iPad.
Solution 2: Subterranean & Biophilic Mastery — walk-out basements, climate-controlled wine cellars, recovery suites, quiet tech integration, biophilic sourcing with local raw cedar and Squamish basalt.
The Foreman Guarantee: Fixed-price, performance-bonded PM agreements. WCB Prime Contractor liabilities handled. Geotech/Civil engineer coordination. Municipal revision backlog clearing.

SECTION 3: $1.55M MEXICO RETREAT INVESTOR PITCH DECK
Capital raise for clinical-grade longevity and wellness compound in Merida/Mexico.
Total Capital Raise: $1.55M USD.
Target: High-performing entrepreneurs and executives over 40 to reset biological age.
Architectural Specs: Zoned architectural kitchens, discrete linear lighting, limewash plaster walls, subterranean wellness suite (3C cold plunges, saunas, hyperbaric oxygen chambers).
Financial Metrics: Projected 22.4% IRR for equity partners with structured buyout option in Year 3.
Use of Funds: Land acquisition, foundation pours, local construction trades, off-grid power/water systems.

SECTION 4: CINEMATIC STORYBOARD & GOOGLE FLOW PROMPT LIBRARY
Artist Character Ingredients Lock (Midjourney/Flux):
A rugged, athletic 43-year-old contractor, short clean-cut graying hair, sharp jawline, dressed in charcoal gray technical canvas shirt, standing on custom timber construction site in Squamish BC. Cinematic lighting, morning mountain fog, shot on Arri Alexa 65, 85mm lens, photorealistic.

Google Flow (Veo 3.1) Motion Prompts:
Cold Plunge: Slow cinematic dolly-in of man stepping into outdoor concrete cold plunge pool, misty forest, Squamish mountains.
Subterranean Great Room: Glide-through camera revealing modern luxury walk-out basement, limewash plaster, warm walnut cabinetry, discrete fireplace.
Builder Sequence: Over-the-shoulder macro tracking shot of hands unrolling blueprint on raw timber workbench.

SECTION 5: SUPABASE MULTI-TENANT DATABASE SCHEMA
PostgreSQL provisions for Progress Web App on Supabase with strict multi-tenant silos (RBAC) and pgvector memory.
Tables: tenants, projects, trades, milestones, brain_embeddings
HNSW Index: m=24, ef_construction=100 for cosine distance matching
Security: Row Level Security (RLS) on all tables with tenant_isolation_policy

SECTION 6: PROGRAMMATIC AUDIOBOOK & VOICE CLONE PIPELINE
ElevenLabs API voice clone pipeline for turning written SOPs and case studies into audiobooks.
4-Step Pipeline: Context Slicing (5000 char chunks) -> ElevenLabs TTS (stability 0.75, clarity 0.85) -> ffmpeg concatenation -> ID3 metadata tagging and distribution to Google Drive/YouTube/Substack.
"""

# Chunk the document
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(MASTER_DOC)
metadata = [{"source": "Keystone_Empire_Master_Strategy_Manual_May2026.gdoc", "section": "master_strategy"} for _ in chunks]

print(f"Ingesting {len(chunks)} chunks into 'master' namespace...")
client.add(collection_name="master", documents=chunks, metadata=metadata)
print("Done! Master Strategy Manual ingested into brain.")

# Also put construction-specific content into possibilities namespace
possibilities_content = MASTER_DOC.split("SECTION 3")[0]  # Sections 1-2
p_chunks = chunk_text(possibilities_content)
p_meta = [{"source": "Master_Strategy_Possibilities_Extract", "section": "web_architecture_and_copy"} for _ in p_chunks]
print(f"\nIngesting {len(p_chunks)} chunks into 'possibilities' namespace...")
client.add(collection_name="possibilities", documents=p_chunks, metadata=p_meta)
print("Done! Possibilities-specific content ingested.")

# Protocol/retreat content
protocol_content = MASTER_DOC.split("SECTION 3")[1].split("SECTION 5")[0]
pr_chunks = chunk_text(protocol_content)
pr_meta = [{"source": "Master_Strategy_Protocol_Extract", "section": "retreat_and_content"} for _ in pr_chunks]
print(f"\nIngesting {len(pr_chunks)} chunks into 'protocol' namespace...")
client.add(collection_name="protocol", documents=pr_chunks, metadata=pr_meta)
print("Done! Protocol-specific content ingested.")
