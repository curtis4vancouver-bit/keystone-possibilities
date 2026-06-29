import os
import datetime
import shutil
from qdrant_client import QdrantClient

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
DEEP_RESULTS_DIR = os.path.join(PROJECT_ROOT, "Deep_Research_Results")
RESEARCH_ARCHIVES = os.path.join(PROJECT_ROOT, "Research_Archives")

# Initialize client
client = QdrantClient(url="http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5")

collection_name = "keystone_brain"

# Complete 32 files ingestion mapping
files_to_ingest = [
    # Pillar 1 - Technical SEO
    ("1_1_Core_Web_Vitals.md", "webmaster"),
    ("1_2_Schema_Markup.md", "webmaster"),
    ("1_3_Technical_SEO_Audit_Checklist.md", "webmaster"),
    ("1_4_Hosting_Constraints.md", "webmaster"),
    # Pillar 1 - Local SEO
    ("2_1_Google_Business_Profile.md", "local_seo"),
    ("2_2_Local_Citation_Building.md", "local_seo"),
    ("2_3_Review_Strategy.md", "local_seo"),
    ("2_4_Local_Link_Building.md", "local_seo"),
    # Pillar 1 - GEO
    ("3_1_AI_Search_Sourcing.md", "webmaster"),
    ("3_2_Content_Strategy_AI.md", "webmaster"),
    ("3_3_Knowledge_Panel.md", "webmaster"),
    ("3_4_Schema_Markup_GEO.md", "webmaster"),
    # Pillar 1 - On-Page
    ("4_1_Service_Page_Architecture.md", "webmaster"),
    ("4_2_Blog_Content_Strategy.md", "webmaster"),
    ("4_3_Landing_Page_Conversion.md", "webmaster"),
    # Pillar 1 - Competitive
    ("5_1_Competitor_Analysis.md", "local_seo"),
    
    # Pillar 2 - Research & Scripting
    ("6_1_AI_Assisted_Research_Verification.md", "content_pipeline"),
    ("6_2_YouTube_Scriptwriting_Best_Practices.md", "content_pipeline"),
    ("6_3_YouTube_Thumbnail_Title_Optimization.md", "content_pipeline"),
    # Pillar 2 - Google Flow
    ("7_1_Google_Flow_Feature_Reference.md", "music"),
    ("7_2_Prompt_Engineering_AI_Video.md", "music"),
    ("7_3_Character_Consistency_AI_Video.md", "music"),
    # Pillar 2 - DaVinci Resolve
    ("8_1_DaVinci_Resolve_Workflow.md", "music"),
    ("8_2_DaVinci_Scripting_API.md", "music"),
    # Pillar 2 - Multi-platform Upload
    ("9_1_YouTube_Upload_Metadata_AI_Disclosure.md", "content_pipeline"),
    ("9_2_YouTube_Shorts_2026_Optimization.md", "content_pipeline"),
    ("9_3_TikTok_Upload_Requirements.md", "content_pipeline"),
    ("9_4_Instagram_Reels_Requirements.md", "content_pipeline"),
    ("9_5_Facebook_Video_Requirements.md", "content_pipeline"),
    ("9_6_Multi_Platform_Upload_Automation.md", "content_pipeline"),
    # Pillar 2 - Blog Loop
    ("10_1_Video_to_Blog_Loop.md", "webmaster"),
    ("10_2_Blog_SEO_Checklist.md", "webmaster"),
]

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def main():
    print("Starting direct Qdrant ingestion of pending reports...")
    
    # Ensure collection exists
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    if collection_name not in collection_names:
        print(f"Creating Qdrant collection '{collection_name}'...")
    
    for filename, namespace in files_to_ingest:
        src_path = os.path.join(DEEP_RESULTS_DIR, filename)
        if not os.path.exists(src_path):
            continue
            
        print(f"\nProcessing {filename} -> namespace: '{namespace}'...")
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        chunks = chunk_text(content)
        print(f"Chunked into {len(chunks)} fragments.")
        
        documents = []
        metadata_list = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadata_list.append({
                "document": chunk,
                "namespace": namespace,
                "source": f"deep_research/{os.path.splitext(filename)[0]}",
                "filename": filename,
                "chunk_index": i,
                "created_at": datetime.datetime.now().isoformat()
            })
            
        # Upload to Qdrant
        print(f"Uploading to Qdrant collection '{collection_name}'...")
        client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata_list
        )
        
        # Archive the file
        dest_path = os.path.join(RESEARCH_ARCHIVES, filename)
        print(f"Archiving to {dest_path}")
        shutil.move(src_path, dest_path)
        print(f"Successfully ingested and archived {filename}")

    print("\nAll pending reports successfully processed!")

if __name__ == "__main__":
    main()
