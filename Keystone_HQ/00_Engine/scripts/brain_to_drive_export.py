"""
Brain-to-Drive Export Script
Exports all Qdrant vector brain namespaces to organized markdown files.
These files are then uploaded to Google Drive for Spark/NotebookLM access.

Usage:
    python brain_to_drive_export.py --export-dir ./brain_export
    python brain_to_drive_export.py --namespace general --limit 50
    python brain_to_drive_export.py --list
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "Qdrant_Brain"))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from qdrant_client import QdrantClient, models
except ImportError:
    print("ERROR: qdrant-client not installed. Run: pip install qdrant-client[fastembed]")
    sys.exit(1)

# Qdrant connection
QDRANT_PATH = str(Path(__file__).parent.parent / "Qdrant_Brain" / "qdrant_storage")
EXPORT_DIR = str(Path(__file__).parent.parent / "scratch" / "brain_export")

# Namespace groupings for organized export
NAMESPACE_GROUPS = {
    "01_Brand_Identity": ["possibilities", "protocol", "music", "brand_avatars"],
    "02_Content_Pipeline": ["content_pipeline", "content_pipeline_v2", "production_pipeline", "production_workflows", "google_flow"],
    "03_SEO_Marketing": ["local_seo", "webmaster", "recomposition_brand_push", "possibilities_leads"],
    "04_Operations": ["master", "operational_playbooks", "corrections", "self_healing", "skills"],
    "05_Agent_Architecture": ["agent_arch", "agent_arch_v2", "keystone_learnings"],
    "06_Knowledge_Base": ["general", "keystone_brain", "keystone_website"],
}

# Skip empty namespaces
SKIP_NAMESPACES = ["legal_counsel", "research_scout", "site_superintendent", "tax_strategist"]

ACTIVE_NAMESPACES = ["possibilities", "protocol_brand", "music", "content_pipeline", "local_seo", "webmaster", "general", "master"]


def get_client():
    """Connect to local Qdrant server."""
    return QdrantClient(url="http://localhost:6333")


def list_namespaces(client):
    """List all namespaces with vector counts from unified collection."""
    print(f"\n{'Namespace':<30} {'Vectors':>10}")
    print("-" * 42)
    total = 0
    for ns in sorted(ACTIVE_NAMESPACES):
        try:
            count_res = client.count(
                collection_name="keystone_unified",
                count_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns)
                        )
                    ]
                ),
                exact=True
            )
            count = count_res.count
        except Exception:
            count = 0
        total += count
        print(f"{ns:<30} {count:>10}")
    print("-" * 42)
    print(f"{'TOTAL (Unified)':<30} {total:>10}")


def export_namespace(client, namespace, limit=100):
    """Export a namespace's content to markdown from unified collection."""
    try:
        # Count points for this tenant
        count_res = client.count(
            collection_name="keystone_unified",
            count_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=namespace)
                    )
                ]
            ),
            exact=True
        )
        total_points = count_res.count
    except Exception:
        return None
    
    if total_points == 0:
        return None
    
    # Scroll through points filtering by tenant_id
    all_points = []
    offset = None
    remaining = min(limit, total_points)
    
    scroll_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=namespace)
            )
        ]
    )
    
    while remaining > 0:
        batch_size = min(remaining, 100)
        try:
            points, next_offset = client.scroll(
                collection_name="keystone_unified",
                scroll_filter=scroll_filter,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            all_points.extend(points)
            remaining -= len(points)
            if next_offset is None or len(points) == 0:
                break
            offset = next_offset
        except Exception as e:
            print(f"Error scrolling namespace {namespace}: {e}")
            break
    
    if not all_points:
        return None
    
    # Build markdown
    lines = [
        f"# Keystone Brain — {namespace}",
        f"",
        f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Vectors:** {total_points}",
        f"**Exported Entries:** {len(all_points)}",
        f"",
        f"---",
        f"",
    ]
    
    for idx, point in enumerate(all_points):
        payload = point.payload or {}
        source = payload.get('source', 'Unknown')
        content = payload.get('document', payload.get('text', ''))
        created = payload.get('created_at', 'N/A')
        
        if not content:
            content = json.dumps(payload, indent=2, default=str)
        
        lines.append(f"## Entry {idx + 1}")
        lines.append(f"**Source:** {source}")
        if created != 'N/A':
            lines.append(f"**Created:** {created}")
        lines.append(f"")
        lines.append(str(content))
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
    
    return "\n".join(lines)


def export_all(client, export_dir, limit_per_namespace=200):
    """Export all namespaces to organized markdown files."""
    os.makedirs(export_dir, exist_ok=True)
    
    exported = []
    skipped = []
    
    for ns in sorted(ACTIVE_NAMESPACES):
        if ns in SKIP_NAMESPACES:
            skipped.append(ns)
            continue
        
        print(f"  Exporting {ns}...", end=" ", flush=True)
        content = export_namespace(client, ns, limit=limit_per_namespace)
        
        if content:
            filepath = os.path.join(export_dir, f"{ns}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            size_kb = len(content) / 1024
            print(f"[OK] ({size_kb:.1f} KB)")
            exported.append((ns, filepath, size_kb))
        else:
            print("(empty, skipped)")
            skipped.append(ns)
    
    # Write index file
    index_lines = [
        "# Keystone Master Brain — Export Index",
        "",
        f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Namespaces exported:** {len(exported)}",
        f"**Namespaces skipped:** {len(skipped)}",
        "",
        "## Exported Namespaces",
        "",
        "| Namespace | Size |",
        "|-----------|------|",
    ]
    for ns, fp, size in exported:
        index_lines.append(f"| {ns} | {size:.1f} KB |")
    
    if skipped:
        index_lines.extend([
            "",
            "## Skipped (empty)",
            "",
        ])
        for ns in skipped:
            index_lines.append(f"- {ns}")
    
    index_lines.extend([
        "",
        "## Namespace Groups",
        "",
    ])
    for group, namespaces in NAMESPACE_GROUPS.items():
        index_lines.append(f"### {group}")
        for ns in namespaces:
            status = "✓" if any(e[0] == ns for e in exported) else "○"
            index_lines.append(f"- {status} {ns}")
        index_lines.append("")
    
    index_path = os.path.join(export_dir, "_INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))
    
    print(f"\n[OK] Export complete: {len(exported)} namespaces -> {export_dir}")
    print(f"  Index: {index_path}")
    return exported


def main():
    parser = argparse.ArgumentParser(description="Export Qdrant brain to Drive-ready files")
    parser.add_argument("--list", action="store_true", help="List all namespaces")
    parser.add_argument("--export-dir", default=EXPORT_DIR, help="Export directory")
    parser.add_argument("--namespace", help="Export single namespace")
    parser.add_argument("--limit", type=int, default=200, help="Max entries per namespace")
    args = parser.parse_args()
    
    client = get_client()
    
    if args.list:
        list_namespaces(client)
        return
    
    if args.namespace:
        os.makedirs(args.export_dir, exist_ok=True)
        content = export_namespace(client, args.namespace, limit=args.limit)
        if content:
            filepath = os.path.join(args.export_dir, f"{args.namespace}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[OK] Exported {args.namespace} -> {filepath}")
        else:
            print(f"[FAIL] Namespace '{args.namespace}' is empty or doesn't exist")
        return
    
    print("Exporting all brain namespaces...")
    export_all(client, args.export_dir, limit_per_namespace=args.limit)


if __name__ == "__main__":
    main()
