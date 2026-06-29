"""
Organize Research_Archives into proper subdirectories.
- Delete DRY RUN stubs (no real content)
- Move content production files (scripts, shot lists) to Content_Production/
- Organize research by category subdirectories
- Move non-research files out of Deep_Research_Results/
"""
import os
import shutil

BASE = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
ARCHIVES = os.path.join(BASE, "Research_Archives")

# === FILES TO DELETE (DRY RUN stubs with no real content) ===
DELETE = [
    "20260521_antigravity_optimization_antigravity_agent_subagent_orchestration_best_practices_and_.md",
    "20260521_antigravity_optimization_antigravity_mcp_server_connection_pooling_and_caching_strate.md",
    "20260521_antigravity_optimization_antigravity_workspace_performance_tuning_and_optimization_tr.md",
    "20260521_antigravity_optimization_gemini_flash_3.5_vs_pro_vs_ultra_model_selection_for_differe.md",
    "20260521_antigravity_optimization_how_to_reduce_antigravity_quota_consumption_per_task.md",
    "20260521_vector_brain_optimization_sqlite-vec_hnsw_index_tuning_for_sub-10ms_retrieval_at_100k_.md",
    "Headless_Browser_Automation_Strategy.md",
]

# === CONTENT PRODUCTION FILES (not research — move to Content_Production/) ===
CONTENT_PROD = [
    "MUSIC_001_ANA_STEVENSON_DJ_SET.md",
    "MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md",
    "MUSIC_002_FLASH_EXECUTION_GUIDE.md",
    "MUSIC_PROVEN_FLOW_PROMPTS.md",
    "POSS_001_BC_HYDRO_CIVIL_CONTRACTOR.md",
    "POSS_001_BROLL_SHOT_LIST.md",
    "POSS_001_GOOGLE_FLOW_SEGMENTS.md",
    "POSS_002_20S_SHORT_BILL44.md",
    "POSS_002_SHORT_BC_HYDRO_CIVIL.md",
    "RECOMPOSITION_BLACK_ROOM_BACKGROUND_PROMPT.md",
    "SCRIPT_001_BROLL_SHOT_LIST.md",
    "SCRIPT_001_CLEAN_READ.md",
    "SCRIPT_001_GLP1_MUSCLE_LOSS_BUILDER_BLUEPRINT.md",
    "SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md",
    "SCRIPT_002_SHORT_GLP1_MUSCLE_LOSS.md",
    "SCRIPT_003_SHORT_CJC_VS_TESAMORELIN.md",
    "SHORT_001_BPC157_SEMAGLUTIDE_STACK.md",
    "SHORT_002_CREATINE_LIES.md",
]

# === INFRASTRUCTURE DOCS (move to Master_Docs/) ===
INFRA_DOCS = [
    "20_SOCIAL_MEDIA_INFRASTRUCTURE_MASTER.md",
]

# === RENAME this badly-named file ===
RENAME = {
    "Extracted_You saidAdvanced RAG and vec_1778475011.md": "20260607_CODING_OPT_advanced_rag_pgvector_hnsw_optimization.md",
}

# === CATEGORIZE remaining research into subdirectories ===
CATEGORIES = {
    "01_Agent_Architecture": [
        "20260609_AGENT_ARCH_",
        "20260521_hermes_agent_analysis_",
        "20260522_hermes_",
        "20260521_self_learning_patterns_",
        "20260522_self_learning_patterns_",
        "20260522_error_driven_learning_",
        "20260522_autonomous_skill_creation_",
        "20260522_antigravity_skills_discovery_",
        "20260522_antigravity_custom_skills",
        "20260522_antigravity_skills_directory",
        "Agentic_MCP_Architecture_Blueprint",
        "03_self_evolving_local_braintrust",
    ],
    "02_MCP_Tools": [
        "20260609_MCP_TOOLS_",
        "20260522_mcp_ecosystem_",
        "20260522_mcp_business_automation",
        "20260522_fastmcp_custom_servers",
        "01_mcp_and_workstation_optimization",
        "02_gemini_agent_local_integration",
    ],
    "03_YouTube_Scripts": [
        "20260609_YOUTUBE_SCRIPTS_",
        "20260610_YOUTUBE_SCRIPTS_",
        "6_2_YouTube_Scriptwriting_Best_Practices",
        "6_3_YouTube_Thumbnail_Title_Optimization",
    ],
    "04_YT_Analytics": [
        "20260610_YT_ANALYTICS_",
        "20260522_youtube_algorithm_",
        "20260522_youtube_api_channel_switching",
        "08_youtube_wellness_content_engine",
    ],
    "05_Video_Production": [
        "20260610_VIDEO_PROD_",
        "20260522_davinci_resolve_",
        "DaVinci_Resolve_Timeline_Automation",
        "davinci_resolve_api_automation_research_plan",
        "davinci_resolve_mcp_v2_architecture",
        "7_1_Google_Flow_Feature_Reference",
        "7_2_Prompt_Engineering_AI_Video",
        "7_3_Character_Consistency_AI_Video",
        "8_1_DaVinci_Resolve_Workflow",
        "8_2_DaVinci_Scripting_API",
    ],
    "06_Deep_House_Music": [
        # None completed yet from this category
    ],
    "07_Coding_Optimization": [
        "20260522_embedding_chunk_optimization",
        "20260522_embedding_model_comparison",
        "20260522_incremental_ingestion",
        "20260522_vector_threshold_tuning",
        "Windows_11_High_Concurrency_Optimization",
    ],
    "08_SEO_Website": [
        "1_1_Core_Web_Vitals",
        "1_2_Schema_Markup",
        "1_3_Technical_SEO_Audit_Checklist",
        "1_4_Hosting_Constraints",
        "2_2_Local_Citation_Building",
        "2_3_Review_Strategy",
        "2_4_Local_Link_Building",
        "2_1_Google_Business_Profile",
        "3_1_AI_Search_Sourcing",
        "3_2_Content_Strategy_AI",
        "3_3_Knowledge_Panel",
        "3_4_Schema_Markup_GEO",
        "4_1_Service_Page_Architecture",
        "4_2_Blog_Content_Strategy",
        "4_3_Landing_Page_Conversion",
        "5_1_Competitor_Analysis",
        "07_local_seo_civil_construction",
        "09_reddit_competitor_intelligence",
        "10_1_Video_to_Blog_Loop",
        "10_2_Blog_SEO_Checklist",
        "20260522_competitor_tag_hijack_analysis",
        "Keystone_Brand_Infrastructure_Scaling",
    ],
    "09_Social_Media": [
        "20260522_social_media_automation_",
        "20260522_social_token_rotation_monitoring",
        "20260522_meta_reels_publishing_complete",
        "20260522_tiktok_content_posting_api_complete",
        "20260521_self_correction_tonight_meta_graph_api_",
        "9_1_YouTube_Upload_Metadata_AI_Disclosure",
        "9_2_YouTube_Shorts_2026_Optimization",
        "9_3_TikTok_Upload_Requirements",
        "9_4_Instagram_Reels_Requirements",
        "9_5_Facebook_Video_Requirements",
        "9_6_Multi_Platform_Upload_Automation",
    ],
    "10_Tax_Legal_Corporate": [
        "04_cra_cerb_dividend_dispute",
        "05_bc_dividend_salary_tax_model",
        "06_cra_taxpayer_relief_guide",
        "11_bc_court_audio_admissibility",
        "12_corporate_asset_shielding_model",
        "17_corporate_shielding_and_voice_ip_blueprint",
        "bc_contractor_tax_compliance",
        "20260522_canadian_tax_optimization",
        "20260522_worksafebc_contractor_obligations",
    ],
    "11_Security": [
        "20260522_security_hardening_",
    ],
    "12_Branding_Marketing": [
        "20260521_low_cost_branding_",
        "20260522_low_cost_branding_",
        "20260521_shopify_audiobook_marketing_",
        "20260522_shopify_audiobook_",
        "creative_media_playbook",
        "Opus_Level_Copywriting_Framework",
    ],
    "13_Chrome_Automation": [
        "20260522_chrome_automation_",
        "20260522_chrome_devtools_advanced",
        "20260522_google_deep_research_automation",
        "20260522_overnight_scheduler_daemon",
    ],
    "14_Gemini_Platform": [
        "20260522_gemini_platform_",
    ],
    "15_Content_Pipeline": [
        "10_omi_companion_voice_archiver",
        "13_omi_dynamic_video_automation",
        "14_high_retention_video_psychology",
        "20260522_mock_test_self_evaluation",
        "omi_workstation_efficacy",
        "yt_dlp_mcp_integration_guide",
        "playwright_marketplace_automation_strategy",
        "6_1_AI_Assisted_Research_Verification",
    ],
    "16_Wellness_Retreat": [
        "15_biophilic_resort_visual_narrative",
        "16_biophilic_resort_jv_blueprint",
        "18_wellness_economics_mexico_expansion",
        "2026-06-08_wellness_retreat_strategy",
        "Mexico_Longevity_Investment_Pitch",
    ],
    "17_BC_Construction": [
        "BC_Building_Code_Memory_Integration",
    ],
}


def categorize_file(filename):
    """Find which category a file belongs to."""
    for category, prefixes in CATEGORIES.items():
        for prefix in prefixes:
            if filename.startswith(prefix):
                return category
    return None


def main():
    # Stats
    deleted = 0
    moved_prod = 0
    moved_infra = 0
    renamed = 0
    categorized = 0
    uncategorized = []

    # 1. Delete DRY RUN stubs
    for f in DELETE:
        path = os.path.join(ARCHIVES, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"DELETED: {f}")
            deleted += 1

    # 2. Move content production files
    prod_dir = os.path.join(ARCHIVES, "..", "Content_Production")
    os.makedirs(prod_dir, exist_ok=True)
    for f in CONTENT_PROD:
        src = os.path.join(ARCHIVES, f)
        dst = os.path.join(prod_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"MOVED TO Content_Production: {f}")
            moved_prod += 1

    # 3. Move infrastructure docs
    docs_dir = os.path.join(ARCHIVES, "..", "Master_Docs")
    for f in INFRA_DOCS:
        src = os.path.join(ARCHIVES, f)
        dst = os.path.join(docs_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"MOVED TO Master_Docs: {f}")
            moved_infra += 1

    # 4. Rename badly-named files
    for old_name, new_name in RENAME.items():
        src = os.path.join(ARCHIVES, old_name)
        dst = os.path.join(ARCHIVES, new_name)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"RENAMED: {old_name} -> {new_name}")
            renamed += 1

    # 5. Categorize remaining files into subdirectories
    remaining = [f for f in os.listdir(ARCHIVES) if f.endswith('.md') and os.path.isfile(os.path.join(ARCHIVES, f))]
    
    for f in remaining:
        cat = categorize_file(f)
        if cat:
            cat_dir = os.path.join(ARCHIVES, cat)
            os.makedirs(cat_dir, exist_ok=True)
            src = os.path.join(ARCHIVES, f)
            dst = os.path.join(cat_dir, f)
            shutil.move(src, dst)
            categorized += 1
        else:
            uncategorized.append(f)

    # 6. Clean up Deep_Research_Results (move non-research files)
    dr_dir = os.path.join(BASE, "Deep_Research_Results")
    for f in os.listdir(dr_dir):
        if not f.endswith('.md'):
            src = os.path.join(dr_dir, f)
            dst = os.path.join(BASE, "scratch", f)
            shutil.move(src, dst)
            print(f"MOVED FROM Deep_Research_Results to scratch: {f}")

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Deleted (DRY RUN stubs):     {deleted}")
    print(f"  Moved to Content_Production: {moved_prod}")
    print(f"  Moved to Master_Docs:        {moved_infra}")
    print(f"  Renamed:                     {renamed}")
    print(f"  Categorized into subdirs:    {categorized}")
    print(f"  Uncategorized (left in root):{len(uncategorized)}")
    if uncategorized:
        print(f"\n  UNCATEGORIZED FILES:")
        for f in sorted(uncategorized):
            print(f"    - {f}")


if __name__ == "__main__":
    main()
