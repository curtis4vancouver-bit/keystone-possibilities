"""
Nightly Research Scheduler
===========================

Generates Chrome deep research prompts based on a weekly topic rotation.
Outputs a JSON file that the ``keystone-chrome-research-automation``
skill consumes to run 3-tab deep research sessions.

Usage:
    python nightly_research_scheduler.py
"""

import json
from datetime import datetime
from pathlib import Path

from config import RESEARCH_DOCS, LEARNINGS, logger, ensure_directories


# ---------------------------------------------------------─
# WEEKLY ROTATION (0=Monday … 6=Sunday)
# ---------------------------------------------------------─
WEEKLY_SCHEDULE: dict[int, dict] = {
    0: {
        "topic":     "BC Building Codes & Step Code",
        "namespace": "possibilities",
        "doc":       RESEARCH_DOCS["building_codes"],
        "prompts": [
            "Deep research the latest BC Building Code 2024 amendments effective in 2026, "
            "focusing on Energy Step Code 3 and 4 requirements for climate zone 4 "
            "(Sea-to-Sky corridor). Include airtightness targets, HRV specifications, "
            "and heat pump mandates.",

            "Deep research Bill 44 SSMUH implementation status in BC municipalities "
            "as of June 2026. Which Sea-to-Sky municipalities have completed zoning "
            "alignment? What are the penalties for non-compliance after June 30 2026?",

            "Deep research BC zero carbon step code requirements for new residential "
            "construction in Squamish and Whistler. What fossil fuel restrictions apply? "
            "What heat pump specifications are mandatory?",
        ],
    },
    1: {
        "topic":     "SEO & Generative Engine Optimization",
        "namespace": "master",
        "doc":       RESEARCH_DOCS["seo_trends"],
        "prompts": [
            "Deep research the latest Google algorithm changes in June 2026. "
            "What are the new Core Web Vitals thresholds? How has INP replaced FID? "
            "What are the best practices for passing INP?",

            "Deep research Generative Engine Optimization (GEO) best practices "
            "for local service businesses in 2026. How do you optimize for Google "
            "AI Overviews, Perplexity citations, and Claude answer blocks?",

            "Deep research local SEO ranking factors for construction companies "
            "in British Columbia in 2026. What Google Business Profile features "
            "drive the most calls and form submissions?",
        ],
    },
    2: {
        "topic":     "Property, Land & Realtor Leads",
        "namespace": "possibilities",
        "doc":       RESEARCH_DOCS["client_strategies"],
        "prompts": [
            "Deep research current commercial and rural land opportunities in the "
            "Sea-to-Sky corridor suitable for retreat centres or multi-unit residential. "
            "Include zoning classifications and recent sales comparables.",

            "Deep research new residential subdivision developments announced in "
            "Squamish and Whistler for 2026-2028. Which developers are active? "
            "What civil construction contracts are upcoming?",

            "Deep research the top-producing real estate agents in the Sea-to-Sky "
            "corridor. Who handles the most new construction listings? "
            "Which brokerages are growing fastest?",
        ],
    },
    3: {
        "topic":     "AI Systems, MCP & Agent Architecture",
        "namespace": "master",
        "doc":       RESEARCH_DOCS["ai_systems"],
        "prompts": [
            "Deep research the latest advancements in Model Context Protocol (MCP) "
            "servers and autonomous agent architectures as of June 2026. What new "
            "MCP servers have been released? What are the best practices for "
            "multi-agent coordination?",

            "Deep research Google Gemini 3.5 Pro capabilities and API pricing. "
            "What is the context window? What new features are available for "
            "developers on the Ultra plan?",

            "Deep research the state of AI code agents in June 2026. Compare "
            "Antigravity, Cursor, Windsurf, and Codex. Which supports the most "
            "MCP integrations and autonomous workflows?",
        ],
    },
    4: {
        "topic":     "Music Production & Streaming Strategy",
        "namespace": "music",
        "doc":       RESEARCH_DOCS["music_trends"],
        "prompts": [
            "Deep research Spotify algorithmic playlist placement strategies "
            "for ambient and 432 Hz frequency music in 2026. What submission "
            "platforms have the highest acceptance rates?",

            "Deep research the current state of AI-generated music copyright "
            "and licensing in Canada and the US as of 2026. Can AI music be "
            "copyrighted? What are the ISRC requirements?",

            "Deep research YouTube Music monetization requirements and best "
            "practices for ambient/focus music channels in 2026.",
        ],
    },
    5: {
        "topic":     "Competitors, Social & Brand Strategy",
        "namespace": "master",
        "doc":       RESEARCH_DOCS["social_trending"],
        "prompts": [
            "Deep research the most effective short-form video hooks and visual "
            "retention strategies for health optimization content in 2026. "
            "What thumbnail styles get the highest CTR?",

            "Deep research TikTok and Instagram Reels algorithm changes in "
            "June 2026. What posting frequency, hashtag strategies, and "
            "content formats drive the most organic reach?",

            "Deep research the top 10 health and biohacking YouTube channels "
            "in 2026. What are their subscriber counts, posting frequencies, "
            "and content strategies?",
        ],
    },
    6: {
        "topic":     "Legal, Tax & WorkSafeBC Compliance",
        "namespace": "possibilities",
        "doc":       RESEARCH_DOCS["contractor_audit"],
        "prompts": [
            "Deep research WorkSafeBC compliance requirements and 2026 premium "
            "rate changes for civil contractors in BC. What are the new safety "
            "training mandates?",

            "Deep research Canadian small business tax deductions for 2026 "
            "applicable to construction companies. What new CRA rules apply "
            "to home office, vehicle, and equipment deductions?",

            "Deep research BC contractor licensing requirements updated in "
            "2026. What changes have been made to the Homeowner Protection Act "
            "and National Home Warranty program?",
        ],
    },
}


def generate_research_prompts() -> Path:
    """
    Generate tonight's deep research prompts based on the day of the week.
    Returns the path to the generated JSON file.
    """
    logger.info("=== NIGHTLY RESEARCH SCHEDULER ===")
    ensure_directories()

    day_of_week = datetime.now().weekday()  # 0=Monday … 6=Sunday
    tonight = WEEKLY_SCHEDULE.get(day_of_week, WEEKLY_SCHEDULE[0])

    logger.info("Day %d → Topic: %s (Namespace: %s)",
                day_of_week, tonight["topic"], tonight["namespace"])

    prompts_data = {
        "date":          datetime.now().isoformat(),
        "day_of_week":   day_of_week,
        "topic":         tonight["topic"],
        "namespace":     tonight["namespace"],
        "target_doc":    tonight["doc"],
        "prompt_count":  len(tonight["prompts"]),
        "prompts":       tonight["prompts"],
    }

    output_file = LEARNINGS / "tonight_research_prompts.json"
    output_file.write_text(
        json.dumps(prompts_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    logger.info("Generated %d prompts. Saved to: %s",
                len(tonight["prompts"]), output_file.name)
    logger.info("The 'keystone-chrome-research-automation' skill will execute these.")

    return output_file


if __name__ == "__main__":
    generate_research_prompts()
