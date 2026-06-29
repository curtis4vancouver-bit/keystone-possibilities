import os

SKILLS_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\dynamic_skills"

agents = {
    "01_chronos_master_brain": "Master Brain orchestration. Loops through other agents, checks status, and triggers self-healing.",
    "02_keystone_possibilities": "B2B construction script writing and heavy civil industry research.",
    "03_keystone_uploader": "Uploads media to Keystone Possibilities YouTube, FB, and IG.",
    "04_keystone_local_seo": "Local SEO strategies, GMB optimization for the construction business.",
    "05_youtube_protocol": "Researches data and writes scripts for the YouTube Protocol channel.",
    "06_protocol_uploader": "Uploads Protocol videos to Instagram, Facebook, TikTok, and YouTube.",
    "07_protocol_brand_awareness": "Broader PR and brand campaigns for the Protocol brand.",
    "08_music_creator": "DAW workflows, song structure generation, and music creation.",
    "09_music_uploader": "Dedicated uploader for Keystone Recomposition Music tracks.",
    "10_music_awareness": "PR and brand awareness specifically focused on promoting the music.",
    "11_website_branding": "Managing UI/UX consistency and blog writing for both websites."
}

def generate_skills():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    # Remove old skills
    for f in os.listdir(SKILLS_DIR):
        if f.endswith(".md"):
            os.remove(os.path.join(SKILLS_DIR, f))
    
    for name, desc in agents.items():
        file_path = os.path.join(SKILLS_DIR, f"{name}.md")
        content = f"""---
name: {name}
description: "{desc}"
---

# {name.replace('_', ' ').title()}

## Primary Directives
You are configured as `{name}`.
Your main role is: {desc}

## Standard Operating Procedure
1. Always use the Dynamic Multiplexer `mcp_multiplexer_execute_tool` to interact with external services.
2. Coordinate with Chronos if you encounter a blocked path requiring self-evolution or self-healing.
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {file_path}")

if __name__ == "__main__":
    generate_skills()
