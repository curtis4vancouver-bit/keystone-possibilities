import os
from pathlib import Path
from qdrant_client import QdrantClient, models

def audit_sources():
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "keystone_unified"
    workspace = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
    
    # We know 'general' (11,463) and 'music' (412) load without corruption.
    # These two combined = 11,875 healthy points we can read.
    # The other namespaces crash when scrolled in bulk.
    # Let's read what we can and check if sources exist on disk.
    
    healthy_namespaces = ["general", "music"]
    
    all_sources = {}  # source -> count
    sources_on_disk = 0
    sources_missing = 0
    missing_list = []
    
    for ns in healthy_namespaces:
        print(f"Scanning namespace '{ns}'...")
        res, _ = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=ns)
                    )
                ]
            ),
            limit=15000,
            with_payload=True,
            with_vectors=False
        )
        
        for point in res:
            p = point.payload or {}
            source = p.get("source") or p.get("path") or "unknown"
            doc_type = p.get("type")
            
            if source not in all_sources:
                all_sources[source] = {"count": 0, "type": doc_type, "namespace": ns}
            all_sources[source]["count"] += 1
    
    print(f"\nTotal unique sources found in healthy namespaces: {len(all_sources)}")
    
    # Check if each source exists on disk
    for source, info in sorted(all_sources.items()):
        # Sources are stored as relative paths from workspace root
        full_path = workspace / source
        
        # Some sources are just identifiers, not paths (deep_research/...)
        # Try multiple resolution strategies
        exists = False
        if full_path.exists():
            exists = True
        elif (workspace / source.split("/")[-1]).exists():
            exists = True
        
        if exists:
            sources_on_disk += 1
        else:
            sources_missing += 1
            if len(missing_list) < 30:
                missing_list.append(f"  [{info['namespace']}] {source} ({info['count']} chunks, type={info['type']})")
    
    print(f"\nSources still on disk: {sources_on_disk}")
    print(f"Sources NOT on disk:   {sources_missing}")
    
    if missing_list:
        print(f"\nSample missing sources (first 30):")
        for m in missing_list:
            print(m)
    
    # Now check what the Obsidian ingestion script would pick up
    EXCLUDE_DIRS = {
        ".git", ".obsidian", ".system_generated", "node_modules",
        "scratch", "__pycache__", "app", "davinci-resolve-mcp", "deprecated_scripts"
    }
    
    md_files = []
    for path in workspace.rglob("*.md"):
        rel_parts = path.relative_to(workspace).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue
        md_files.append(path)
    
    print(f"\nMarkdown files Obsidian ingestion would scan: {len(md_files)}")
    
    # How many of the missing sources could be recovered by re-scanning?
    recoverable = 0
    not_recoverable = []
    for source, info in all_sources.items():
        full_path = workspace / source
        if not full_path.exists():
            # Check if any .md file on disk matches the source basename
            basename = source.split("/")[-1]
            found = any(p.name == basename or basename in p.name for p in md_files)
            if found:
                recoverable += 1
            else:
                not_recoverable.append(source)
    
    print(f"Missing sources recoverable by re-scan: {recoverable}")
    print(f"Missing sources NOT recoverable: {len(not_recoverable)}")
    if not_recoverable[:20]:
        print("Sample unrecoverable sources:")
        for s in not_recoverable[:20]:
            print(f"  - {s}")

if __name__ == "__main__":
    audit_sources()
