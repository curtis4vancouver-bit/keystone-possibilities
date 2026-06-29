import os

SKILLS_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\dynamic_skills"

agents = {
    "12_legal_counsel": "Dedicated to legal matters, compliance, and reviewing contracts for the Keystone and Protocol empire.",
    "13_tax_strategist": "Focuses on tax strategies, deductions, and financial structuring for the businesses.",
    "14_property_scout": "Finds properties for retreats. Uses Gemini 3D creator for visualizing layouts and spaces.",
    "15_site_superintendent": "Strictly for active job sites. Checks blueprints, handles step code requirements, and ensures site compliance."
}

def generate_skills():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    
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
1. Always use the Dynamic Multiplexer `mcp_multiplexer_execute_tool` to interact with external services or search for required codes.
2. Coordinate with Chronos if you encounter a blocked path requiring self-evolution.
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {file_path}")

if __name__ == "__main__":
    generate_skills()
