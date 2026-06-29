"""Re-ingest 6 broken brain sources (1 chunk each) from Research_Archives."""
import os
import shutil
import subprocess

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
ARCHIVES = os.path.join(PROJECT_ROOT, "Research_Archives")
RESULTS = os.path.join(PROJECT_ROOT, "Deep_Research_Results")
BRAIN_FEEDER = os.path.join(PROJECT_ROOT, "10_Vector_DB_Architecture", "brain_feeder")
INGEST_JS = os.path.join(BRAIN_FEEDER, "ingest_file.js")

BROKEN_SOURCES = [
    "20260521_antigravity_optimization_antigravity_agent_subagent_orchestration_best_practices_and_.md",
    "20260521_antigravity_optimization_antigravity_mcp_server_connection_pooling_and_caching_strate.md",
    "20260521_antigravity_optimization_antigravity_workspace_performance_tuning_and_optimization_tr.md",
    "20260521_antigravity_optimization_gemini_flash_3.5_vs_pro_vs_ultra_model_selection_for_differe.md",
    "20260521_antigravity_optimization_how_to_reduce_antigravity_quota_consumption_per_task.md",
    "20260521_vector_brain_optimization_sqlite-vec_hnsw_index_tuning_for_sub-10ms_retrieval_at_100k_.md",
]

success = 0
failed = 0

for fname in BROKEN_SOURCES:
    src = os.path.join(ARCHIVES, fname)
    if not os.path.exists(src):
        print(f"SKIP (not found): {fname}")
        failed += 1
        continue

    source_name = os.path.splitext(fname)[0]
    print(f"\nRe-ingesting: {fname}")
    print(f"  Source name: {source_name}")
    print(f"  File size: {os.path.getsize(src)} bytes")

    cmd = ["node", INGEST_JS, src, "--source", source_name]
    result = subprocess.run(cmd, cwd=BRAIN_FEEDER, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        print(f"  OK: {result.stdout.strip()[-200:]}")
        success += 1
    else:
        print(f"  FAILED: {result.stderr.strip()[-200:]}")
        failed += 1

print(f"\n=== Done: {success} re-ingested, {failed} failed ===")
