import os
import shutil

# Target conversation directories
target_folders = [
    "a227476a-cebd-47d1-be5b-8088bd70b9d1",
    "780301f1-4c21-45a7-9acb-ced8f8ca9800",
    "49cc4dbe-ad5e-4ca3-8aa0-5c11a6fa6398",
    "1e17d165-e80b-416f-a1e3-39bbee21667b",
    "a378d858-44fa-45eb-ae56-57c3d12682c1"
]

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"
workspace_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
digest_path = os.path.join(workspace_dir, "Master_Docs", "CONSOLIDATED_BRAIN_HISTORY_DIGEST.md")

print("--- Phase 4: Safe Log Cleanup & Space Recovery ---")

# Guardrail 1: Verify digest file exists and has size
if not os.path.exists(digest_path) or os.path.getsize(digest_path) < 15000:
    print(f"CRITICAL ERROR: Consolidated digest was not found or is too small at {digest_path}!")
    print("Cleanup aborted for safety.")
    exit(1)

print("Guardrail 1 Passed: Permanent consolidated history digest verified.")

# Calculate space to be recovered
total_space_freed = 0
folders_to_delete = []

for folder in target_folders:
    folder_path = os.path.join(brain_dir, folder)
    if os.path.exists(folder_path):
        # Calculate folder size
        size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size += os.path.getsize(fp)
        total_space_freed += size
        folders_to_delete.append(folder_path)
        print(f"Targeted: {folder_path} ({round(size / 1024 / 1024, 2)} MB)")
    else:
        print(f"Skipping: {folder_path} (Already deleted or not found)")

if not folders_to_delete:
    print("No folders found to delete. System is already clean!")
    exit(0)

print(f"Total space to be recovered: {round(total_space_freed / 1024 / 1024, 2)} MB")

# Perform Safe Deletion
print("\nExecuting deletions...")
deleted_count = 0
for folder_path in folders_to_delete:
    try:
        shutil.rmtree(folder_path)
        print(f"Successfully deleted: {folder_path}")
        deleted_count += 1
    except Exception as e:
        print(f"Failed to delete {folder_path}: {e}")

print(f"\nCleanup Complete: Safely removed {deleted_count} redundant chat logs.")
