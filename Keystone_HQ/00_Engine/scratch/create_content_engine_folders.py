# Keystone Content Engine - Desktop Folder Tree Setup
# Programmatically builds the staging directories for Wayne's YouTube videos, shorts, campaigns, and DaVinci assets.

import os

def create_folders():
    desktop_dir = r"C:\Users\Curtis\Desktop"
    base_engine_dir = os.path.join(desktop_dir, "Keystone Content Engine")
    
    # Define exact directory structure
    folder_tree = [
        # 1. Longform Videos (2-3 per week)
        os.path.join(base_engine_dir, "01_Longform_Videos", "Video_1_Staging"),
        os.path.join(base_engine_dir, "01_Longform_Videos", "Video_2_Staging"),
        os.path.join(base_engine_dir, "01_Longform_Videos", "Video_3_Staging"),
        
        # 2. Shorts (4 per week)
        os.path.join(base_engine_dir, "02_Shorts", "Short_1_Staging"),
        os.path.join(base_engine_dir, "02_Shorts", "Short_2_Staging"),
        os.path.join(base_engine_dir, "02_Shorts", "Short_3_Staging"),
        os.path.join(base_engine_dir, "02_Shorts", "Short_4_Staging"),
        
        # 3. Marketing Campaigns & Assets
        os.path.join(base_engine_dir, "03_Campaign_Assets", "Graphics"),
        os.path.join(base_engine_dir, "03_Campaign_Assets", "Copywriting_Drafts"),
        os.path.join(base_engine_dir, "03_Campaign_Assets", "Voiceovers_Raw"),
        
        # 4. DaVinci Resolve Integration
        os.path.join(base_engine_dir, "04_DaVinci_Resolve_Media", "Raw_Footage_Dropzone"),
        os.path.join(base_engine_dir, "04_DaVinci_Resolve_Media", "Render_Output")
    ]
    
    print("="*60)
    print(" BUILDING KEYSTONE DESKTOP CONTENT ENGINE DIRECTORIES ")
    print("="*60)
    
    created_count = 0
    for path in folder_tree:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"  [CREATED] {os.path.relpath(path, desktop_dir)}")
            created_count += 1
        else:
            print(f"  [EXISTS]  {os.path.relpath(path, desktop_dir)}")
            
    print("-"*60)
    print(f"Success: Folders initialized successfully. Created {created_count} new staging directories.")
    print("="*60 + "\n")

if __name__ == "__main__":
    create_folders()
