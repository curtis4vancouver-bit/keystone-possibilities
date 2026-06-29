"""
Keystone Prompt Self-Refiner v1.0 (DSPy-Inspired)
====================================================
Mines the correction_journal.json for recurring error patterns and
automatically generates optimized prevention rules that can be injected
into SKILL.md files — ensuring agents never repeat the same mistakes.

Inspired by Stanford's OpenJarvis on-device learning loop and DSPy
(Declarative Self-Improving Language Programs) trace optimization.

Usage:
  python prompt_refiner.py --analyze              # Show pattern analysis
  python prompt_refiner.py --generate-rules        # Generate prevention rules
  python prompt_refiner.py --inject <skill_path>   # Inject rules into a SKILL.md
  python prompt_refiner.py --full-cycle            # Analyze + generate + report
"""
import os
import sys
import json
import argparse
import datetime
from collections import Counter, defaultdict

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
CORRECTION_JOURNAL = os.path.join(LEARNINGS_DIR, "correction_journal.json")
RULES_OUTPUT = os.path.join(LEARNINGS_DIR, "refined_prevention_rules.json")
INSIGHTS_DIR = os.path.join(LEARNINGS_DIR, "insights")


def load_journal() -> dict:
    """Load the correction journal."""
    if not os.path.exists(CORRECTION_JOURNAL):
        print("[Refiner] No correction journal found.")
        return {"entries": []}
    with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_patterns(journal: dict) -> dict:
    """
    DSPy-style trace analysis: extract recurring failure categories,
    identify the most frequent root causes, and rank prevention rules
    by how many errors they would have prevented.
    """
    entries = journal.get("entries", [])
    if not entries:
        return {"categories": {}, "root_causes": [], "prevention_rules": [], "total": 0}

    # Count by category / error_type
    category_counter = Counter()
    root_cause_counter = Counter()
    prevention_rules = []
    rule_impact = defaultdict(int)  # rule_text -> number of errors it prevents

    for entry in entries:
        # Handle both v1 (id: CJ-001) and v2 (id: CJ-timestamp) formats
        cat = entry.get("category", entry.get("error_type", "unknown"))
        category_counter[cat] += 1

        root = entry.get("root_cause", entry.get("description", ""))
        if root:
            # Normalize to first 80 chars for deduplication
            root_key = root[:80].strip()
            root_cause_counter[root_key] += 1

        # Extract prevention rules
        prev = entry.get("prevention_rule", entry.get("prevention", ""))
        if prev:
            prevention_rules.append({
                "rule": prev,
                "source_category": cat,
                "source_id": entry.get("id", "unknown"),
                "source_date": entry.get("date", entry.get("timestamp", "unknown")),
            })
            rule_impact[prev] += 1

    # Rank categories by frequency
    sorted_categories = dict(category_counter.most_common())

    # Rank root causes
    sorted_roots = [{"cause": k, "count": v} for k, v in root_cause_counter.most_common(10)]

    # Rank prevention rules by impact (how many errors they cover)
    ranked_rules = sorted(prevention_rules, key=lambda r: rule_impact[r["rule"]], reverse=True)

    # Deduplicate rules (keep highest-impact version)
    seen_rules = set()
    unique_rules = []
    for r in ranked_rules:
        rule_text = r["rule"][:100]
        if rule_text not in seen_rules:
            seen_rules.add(rule_text)
            unique_rules.append(r)

    return {
        "total_entries": len(entries),
        "categories": sorted_categories,
        "top_root_causes": sorted_roots,
        "prevention_rules": unique_rules,
        "rule_impact_scores": dict(rule_impact),
    }


def generate_refined_rules(analysis: dict) -> list:
    """
    Synthesizes the analysis into a compact set of machine-readable
    prevention rules that can be injected into any SKILL.md file.
    """
    rules = []
    for idx, rule_data in enumerate(analysis.get("prevention_rules", []), 1):
        rules.append({
            "id": f"PR-{idx:03d}",
            "category": rule_data["source_category"],
            "rule": rule_data["rule"],
            "source": rule_data["source_id"],
            "learned_on": rule_data["source_date"],
            "priority": "HIGH" if analysis["rule_impact_scores"].get(rule_data["rule"], 0) > 1 else "MEDIUM",
        })
    return rules


def save_rules(rules: list):
    """Persist refined rules to disk."""
    os.makedirs(os.path.dirname(RULES_OUTPUT), exist_ok=True)
    payload = {
        "generated_at": datetime.datetime.now().isoformat(),
        "total_rules": len(rules),
        "rules": rules,
    }
    with open(RULES_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[Refiner] Saved {len(rules)} refined prevention rules to: {RULES_OUTPUT}")
    return payload


def generate_skill_injection_block(rules: list) -> str:
    """
    Generates a markdown block that can be appended to any SKILL.md
    to permanently encode learned prevention rules.
    """
    lines = [
        "",
        "---",
        "",
        "## Learned Prevention Rules (Auto-Generated by Prompt Refiner)",
        "",
        "> These rules were automatically extracted from the correction journal.",
        "> They encode hard-won operational lessons. DO NOT remove them.",
        "",
    ]
    for rule in rules:
        priority_icon = "!!!" if rule["priority"] == "HIGH" else "!!"
        lines.append(f"- **[{rule['id']}]** ({priority_icon} {rule['priority']}) `{rule['category']}`: {rule['rule']}")

    lines.append("")
    lines.append(f"_Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")
    return "\n".join(lines)


def inject_into_skill(skill_path: str, rules: list) -> bool:
    """
    Appends the learned prevention rules block to a SKILL.md file.
    If a previous injection block exists, it replaces it.
    """
    if not os.path.exists(skill_path):
        print(f"[Refiner] Skill file not found: {skill_path}")
        return False

    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    injection_block = generate_skill_injection_block(rules)

    # Remove old injection block if present
    marker = "## Learned Prevention Rules (Auto-Generated by Prompt Refiner)"
    if marker in content:
        # Find the start of the old block (the --- before it)
        marker_pos = content.index(marker)
        # Look backwards for the preceding ---
        preceding_hr = content.rfind("\n---\n", 0, marker_pos)
        if preceding_hr == -1:
            preceding_hr = marker_pos
        content = content[:preceding_hr].rstrip()
        print(f"[Refiner] Replaced existing prevention rules block in {skill_path}")
    else:
        print(f"[Refiner] Appending prevention rules block to {skill_path}")

    content = content + injection_block

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def print_analysis_report(analysis: dict):
    """Pretty-print the analysis to the console."""
    print("\n" + "=" * 65)
    print("  PROMPT SELF-REFINER: Correction Journal Analysis")
    print("=" * 65)

    print(f"\n  Total Journal Entries: {analysis['total_entries']}")

    print("\n  Error Categories (by frequency):")
    for cat, count in analysis.get("categories", {}).items():
        bar = "#" * min(count * 3, 30)
        print(f"    {cat:35s} {count:3d}  {bar}")

    print("\n  Top Root Causes:")
    for rc in analysis.get("top_root_causes", [])[:5]:
        print(f"    [{rc['count']}x] {rc['cause']}")

    print(f"\n  Unique Prevention Rules Extracted: {len(analysis.get('prevention_rules', []))}")
    for rule in analysis.get("prevention_rules", [])[:5]:
        print(f"    - [{rule['source_category']}] {rule['rule'][:100]}")

    print("\n" + "=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Keystone Prompt Self-Refiner v1.0")
    parser.add_argument("--analyze", action="store_true", help="Analyze correction journal patterns")
    parser.add_argument("--generate-rules", action="store_true", help="Generate refined prevention rules")
    parser.add_argument("--inject", type=str, help="Inject rules into a SKILL.md file")
    parser.add_argument("--full-cycle", action="store_true", help="Full analysis + generation + report")
    args = parser.parse_args()

    journal = load_journal()
    analysis = analyze_patterns(journal)

    if args.analyze or args.full_cycle:
        print_analysis_report(analysis)

    if args.generate_rules or args.full_cycle:
        rules = generate_refined_rules(analysis)
        save_rules(rules)

        if args.full_cycle:
            # Also generate the insight digest
            os.makedirs(INSIGHTS_DIR, exist_ok=True)
            digest_path = os.path.join(
                INSIGHTS_DIR,
                f"{datetime.date.today().isoformat()}-prompt-refinement.md"
            )
            block = generate_skill_injection_block(rules)
            with open(digest_path, "w", encoding="utf-8") as f:
                f.write(f"# Prompt Refinement Digest - {datetime.date.today()}\n\n")
                f.write(f"Extracted {len(rules)} prevention rules from {analysis['total_entries']} journal entries.\n")
                f.write(block)
            print(f"[Refiner] Digest saved to: {digest_path}")

    if args.inject:
        rules_data = None
        if os.path.exists(RULES_OUTPUT):
            with open(RULES_OUTPUT, "r", encoding="utf-8") as f:
                rules_data = json.load(f)
        else:
            rules = generate_refined_rules(analysis)
            rules_data = {"rules": rules}

        inject_into_skill(args.inject, rules_data["rules"])

    if not any([args.analyze, args.generate_rules, args.inject, args.full_cycle]):
        parser.print_help()


if __name__ == "__main__":
    main()
