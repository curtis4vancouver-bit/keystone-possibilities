"""
Keystone Brain Tenant Consolidation
====================================
Merges 25 fragmented tenants down to 6 canonical tenants.
Uses keyword analysis on the document text to re-classify each vector.
Updates tenant_id in-place (no re-embedding needed).

Before: 25 tenants (general=8013, keystone_brain=3871, master=1052, etc.)
After:  6 canonical tenants (webmaster, content_pipeline, local_seo, music, protocol_brand, possibilities)
"""

from qdrant_client import QdrantClient, models
from collections import Counter
import re

COLLECTION = "keystone_unified"

# The 6 canonical tenants
CANONICAL_TENANTS = {
    "webmaster",        # Agent arch, system optimization, website, SEO infrastructure
    "content_pipeline", # Video production, YouTube, DaVinci, content calendar, uploads
    "local_seo",        # Local SEO, GBP, citations, reviews, Sea-to-Sky
    "music",            # Music production, Spotify, lyrics, avatars, Recomposition music
    "protocol_brand",   # Health, peptides, wellness, Protocol/Recomposition content
    "possibilities",    # Construction brand, PM tips, Bill 44, building code
}

def classify_document(text, source="", filename="", current_tenant=""):
    """Classify a document into the correct canonical tenant based on content analysis."""
    t = (text + " " + source + " " + filename).lower()
    
    # Construction / Possibilities brand
    if any(k in t for k in ["construction", "bill 44", "building code", "step code", "framing",
                             "contractor", "renovation", "home builder", "custom home",
                             "project management", "sea-to-sky", "squamish", "whistler",
                             "pemberton", "site superintendent", "blueline", "rdc fine",
                             "keystone possibilities", "possibilities_brand", "net zero home",
                             "bc energy", "building permit", "general contractor"]):
        return "possibilities"
    
    # Local SEO
    if any(k in t for k in ["local seo", "google business profile", "gbp", "citation",
                             "google maps", "3-pack", "map pack", "review generation",
                             "nap consistency", "houzz", "homestars", "local search",
                             "knowledge panel", "local_seo", "schema markup", "structured data",
                             "video indexing", "watch page", "video sitemap", "search console",
                             "video seo", "json-ld", "videoobject"]):
        return "local_seo"
    
    # Video production & YouTube content pipeline
    if any(k in t for k in ["davinci", "resolve", "timeline", "render", "color grad",
                             "fusion", "subtitle", "caption", "thumbnail", "b-roll",
                             "youtube", "shorts", "upload", "monetiz", "playlist",
                             "content calendar", "publishing cadence", "video prod",
                             "google flow", "omi ai", "elevenlabs", "voice synth",
                             "content_pipeline", "script format", "interview format",
                             "a-roll", "v1/a1", "multicam", "batch download"]):
        return "content_pipeline"
    
    # Music
    if any(k in t for k in ["music", "spotify", "lyrics", "musicbrainz", "streaming",
                             "recomposition music", "avatar", "singing", "vocal",
                             "music_brand", "distrokid", "album", "track listing",
                             "female avatar", "flow prompt"]):
        return "music"
    
    # Protocol / Health / Wellness
    if any(k in t for k in ["protocol", "peptide", "wellness", "health", "ghk-cu",
                             "longevity", "retreat", "biohack", "supplement",
                             "protocol_brand", "recomposition", "apollo engine",
                             "dosage", "clinical", "therapeutic"]):
        return "protocol_brand"
    
    # Agent architecture & system (-> webmaster)
    if any(k in t for k in ["agent", "mcp", "qdrant", "vector", "brain", "embedding",
                             "self-heal", "context window", "instruction drift",
                             "episodic memory", "overnight", "autonomous", "subagent",
                             "skill system", "observability", "gemini api",
                             "security pattern", "circuit breaker", "correction journal",
                             "self_evolution", "chronos"]):
        return "webmaster"
    
    # Website & SEO infrastructure (-> webmaster)
    if any(k in t for k in ["website", "wordpress", "landing page", "woocommerce",
                             "cdn", "caching", "page speed", "core web vitals",
                             "seo", "backlink", "domain authority", "sitemap"]):
        return "webmaster"
    
    # Fallback: try to use current tenant if it's canonical
    if current_tenant in CANONICAL_TENANTS:
        return current_tenant
    
    return "webmaster"  # Ultimate fallback


def main():
    client = QdrantClient(url="http://localhost:6333")
    
    # 1. Read ALL vectors with full payloads
    print("Reading all vectors from keystone_unified...")
    all_points = []
    offset = None
    while True:
        result = client.scroll(
            collection_name=COLLECTION,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        pts, offset = result
        all_points.extend(pts)
        if offset is None:
            break
    
    print(f"Total vectors: {len(all_points)}")
    
    # 2. Classify each point
    reclassified = 0
    already_correct = 0
    updates = []  # (point_id, new_tenant_id)
    
    for pt in all_points:
        current_tenant = pt.payload.get("tenant_id", "unknown")
        doc_text = pt.payload.get("document", pt.payload.get("text", ""))
        source = pt.payload.get("source", "")
        filename = pt.payload.get("filename", "")
        
        if current_tenant in CANONICAL_TENANTS:
            # Already canonical - but let's verify it's correct
            new_tenant = classify_document(doc_text, source, filename, current_tenant)
            if new_tenant == current_tenant:
                already_correct += 1
                continue
            else:
                # Misclassified even though in a canonical tenant
                updates.append((pt.id, new_tenant))
                reclassified += 1
        else:
            # Orphaned tenant - must reclassify
            new_tenant = classify_document(doc_text, source, filename, current_tenant)
            updates.append((pt.id, new_tenant))
            reclassified += 1
    
    print(f"\nAlready correct: {already_correct}")
    print(f"Need reclassification: {reclassified}")
    
    # 3. Show the planned migration
    migration_counts = Counter(new_t for _, new_t in updates)
    print("\nPlanned migrations:")
    for tenant, count in migration_counts.most_common():
        print(f"  -> {tenant}: {count} vectors")
    
    # 4. Execute updates in batches
    print(f"\nExecuting {len(updates)} tenant_id updates...")
    batch_size = 100
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i+batch_size]
        
        # Use set_payload to update just the tenant_id field
        for point_id, new_tenant in batch:
            client.set_payload(
                collection_name=COLLECTION,
                payload={"tenant_id": new_tenant},
                points=[point_id]
            )
        
        done = min(i + batch_size, len(updates))
        print(f"  Updated {done}/{len(updates)} vectors")
    
    # 5. Verify final state
    print("\n--- FINAL TENANT DISTRIBUTION ---")
    final_points = []
    offset = None
    while True:
        result = client.scroll(
            collection_name=COLLECTION,
            limit=100,
            offset=offset,
            with_payload=["tenant_id"],
            with_vectors=False
        )
        pts, offset = result
        final_points.extend(pts)
        if offset is None:
            break
    
    final_tenants = Counter(str(p.payload.get("tenant_id", "MISSING")) for p in final_points)
    for t, count in final_tenants.most_common():
        canonical = "[OK]" if t in CANONICAL_TENANTS else "[UNEXPECTED]"
        print(f"  {t:25s} {count:6d} vectors  {canonical}")
    
    print(f"\nTotal tenants: {len(final_tenants)} (target: {len(CANONICAL_TENANTS)})")
    print("Consolidation complete.")


if __name__ == "__main__":
    main()
