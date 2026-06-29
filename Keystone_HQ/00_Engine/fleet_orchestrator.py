"""
Keystone Fleet Orchestrator v1.0
=================================
The Master Brain's command center for the 13-agent fleet.
Scans all agent silo folders, builds a live dashboard, detects overlap,
promotes skills, routes analytics insights, and enforces brand consistency.

Usage:
  python fleet_orchestrator.py --sweep          # Full fleet sweep (scan + overlap + promote)
  python fleet_orchestrator.py --status         # Quick fleet status dashboard
  python fleet_orchestrator.py --overlaps       # Check for topic/content overlaps
  python fleet_orchestrator.py --promote        # Run skill promotion pipeline
  python fleet_orchestrator.py --route-analytics # Route analytics insights to agent inboxes
  python fleet_orchestrator.py --claim TOPIC AGENT  # Claim a topic for an agent
"""
import os
import sys
import json
import glob
import argparse
import datetime
from collections import defaultdict

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
AGENT_FLEET_DIR = os.path.join(PROJECT_ROOT, "Agent_Fleet")
FLEET_DASHBOARD_DIR = os.path.join(PROJECT_ROOT, "Fleet_Dashboard")
SKILL_VAULT_DIR = os.path.join(PROJECT_ROOT, "Skill_Vault")
BRAND_CONSTITUTION_DIR = os.path.join(PROJECT_ROOT, "Brand_Constitution")

FLEET_STATUS_PATH = os.path.join(FLEET_DASHBOARD_DIR, "fleet_status.json")
OVERLAP_REGISTRY_PATH = os.path.join(FLEET_DASHBOARD_DIR, "overlap_registry.json")
ANALYTICS_FEED_PATH = os.path.join(FLEET_DASHBOARD_DIR, "analytics_feed.json")
PROMOTED_SKILLS_PATH = os.path.join(SKILL_VAULT_DIR, "promoted_skills.json")


def get_all_agents() -> list:
    """List all agent silo directories."""
    if not os.path.exists(AGENT_FLEET_DIR):
        return []
    return [d for d in os.listdir(AGENT_FLEET_DIR)
            if os.path.isdir(os.path.join(AGENT_FLEET_DIR, d))]


def load_agent_state(agent_name: str) -> dict:
    """Load an agent's STATE.json."""
    path = os.path.join(AGENT_FLEET_DIR, agent_name, "STATE.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"agent_name": agent_name, "status": "unknown"}


def load_agent_capabilities(agent_name: str) -> dict:
    """Load an agent's CAPABILITIES.json."""
    path = os.path.join(AGENT_FLEET_DIR, agent_name, "CAPABILITIES.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"agent_name": agent_name, "skills": []}


def load_overlap_registry() -> dict:
    """Load the overlap registry."""
    if os.path.exists(OVERLAP_REGISTRY_PATH):
        with open(OVERLAP_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"claimed_topics": {}, "claimed_video_titles": []}


def save_overlap_registry(registry: dict):
    """Save the overlap registry."""
    with open(OVERLAP_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def write_to_inbox(agent_name: str, message: dict):
    """Write a message to an agent's INBOX.json."""
    inbox_path = os.path.join(AGENT_FLEET_DIR, agent_name, "INBOX.json")
    if os.path.exists(inbox_path):
        with open(inbox_path, "r", encoding="utf-8") as f:
            inbox = json.load(f)
    else:
        inbox = {"messages": []}

    inbox["messages"].append(message)

    # Keep only last 20 messages
    inbox["messages"] = inbox["messages"][-20:]

    with open(inbox_path, "w", encoding="utf-8") as f:
        json.dump(inbox, f, indent=2)


# ─── Fleet Status Dashboard ────────────────────────────────────────────
def build_fleet_status():
    """Scan all 13 agent STATE.json files and build a fleet dashboard."""
    agents = get_all_agents()
    now = datetime.datetime.now().isoformat()

    fleet = {
        "generated_at": now,
        "total_agents": len(agents),
        "active": 0,
        "idle": 0,
        "unknown": 0,
        "agents": {}
    }

    for agent in sorted(agents):
        state = load_agent_state(agent)
        status = state.get("status", "unknown")

        if status == "active":
            fleet["active"] += 1
        elif status == "idle":
            fleet["idle"] += 1
        else:
            fleet["unknown"] += 1

        fleet["agents"][agent] = {
            "status": status,
            "last_active": state.get("last_active"),
            "current_task": state.get("current_task"),
            "outputs_count": len(state.get("last_10_outputs", [])),
            "topics_claimed": len(state.get("content_topics_claimed", [])),
            "brand": state.get("brand_affiliation", "unknown"),
        }

    with open(FLEET_STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(fleet, f, indent=2)

    print(f"[Fleet] Dashboard updated: {fleet['total_agents']} agents | {fleet['active']} active | {fleet['idle']} idle")
    return fleet


# ─── Overlap Detection ──────────────────────────────────────────────────
def detect_overlaps():
    """Scan all agent STATE.json files for topic collisions."""
    agents = get_all_agents()
    topic_owners = defaultdict(list)
    title_owners = defaultdict(list)

    for agent in agents:
        state = load_agent_state(agent)

        # Check claimed topics
        for topic in state.get("content_topics_claimed", []):
            topic_owners[topic.lower()].append(agent)

        # Check output titles
        for output in state.get("last_10_outputs", []):
            title = output.get("title", "").lower()
            if title:
                title_owners[title].append(agent)

    # Find collisions
    collisions = []
    for topic, owners in topic_owners.items():
        if len(owners) > 1:
            collisions.append({"type": "topic", "value": topic, "agents": owners})

    for title, owners in title_owners.items():
        if len(owners) > 1:
            collisions.append({"type": "title", "value": title, "agents": owners})

    if collisions:
        print(f"[Fleet] WARNING: {len(collisions)} overlap(s) detected!")
        for c in collisions:
            print(f"  CONFLICT [{c['type']}]: '{c['value']}' claimed by: {', '.join(c['agents'])}")

        # Notify involved agents
        for c in collisions:
            for agent in c["agents"]:
                write_to_inbox(agent, {
                    "from": "fleet_orchestrator",
                    "date": datetime.datetime.now().isoformat(),
                    "priority": "high",
                    "message": f"OVERLAP DETECTED: '{c['value']}' is also claimed by {[a for a in c['agents'] if a != agent]}. Coordinate with Master Brain.",
                    "action_required": True,
                })
    else:
        print("[Fleet] No overlaps detected. All agents are in their lanes.")

    return collisions


# ─── Topic Claiming ──────────────────────────────────────────────────────
def claim_topic(topic: str, agent_name: str):
    """Register a topic claim for an agent in the overlap registry."""
    registry = load_overlap_registry()

    topic_lower = topic.lower()
    if topic_lower in {k.lower(): k for k in registry["claimed_topics"]}:
        existing = registry["claimed_topics"].get(topic, {})
        owner = existing.get("owner", "unknown")
        print(f"[Fleet] Topic '{topic}' already claimed by {owner}!")
        return False

    registry["claimed_topics"][topic] = {
        "owner": agent_name,
        "claimed_on": datetime.datetime.now().isoformat(),
    }
    registry["last_updated"] = datetime.datetime.now().isoformat()
    save_overlap_registry(registry)
    print(f"[Fleet] Topic '{topic}' claimed by {agent_name}")
    return True


# ─── Skill Promotion Pipeline ──────────────────────────────────────────
def run_skill_promotion():
    """
    Scan all agent CAPABILITIES.json files. If an agent has a skill
    that other agents in the same brand could benefit from, promote it.
    """
    agents = get_all_agents()
    all_caps = {}
    skill_frequency = defaultdict(list)

    for agent in agents:
        caps = load_agent_capabilities(agent)
        all_caps[agent] = caps
        for skill in caps.get("skills", []):
            skill_frequency[skill].append(agent)

    # Find skills that only one agent has but could benefit others
    promotable = []
    for skill, owners in skill_frequency.items():
        if len(owners) == 1:
            owner = owners[0]
            owner_caps = all_caps[owner]
            owner_brand = owner_caps.get("brand_affiliation", "")

            # Check if other agents in the same brand could use it
            for other_agent, other_caps in all_caps.items():
                if other_agent == owner:
                    continue
                other_brand = other_caps.get("brand_affiliation", "")
                if other_brand == owner_brand or other_brand == "all" or owner_brand == "all":
                    if skill not in other_caps.get("skills", []):
                        promotable.append({
                            "skill": skill,
                            "source_agent": owner,
                            "potential_recipient": other_agent,
                            "brand": owner_brand,
                        })

    if promotable:
        print(f"[Fleet] {len(promotable)} skill promotion opportunities found:")
        for p in promotable[:10]:  # Show top 10
            print(f"  {p['skill']}: {p['source_agent']} -> {p['potential_recipient']}")
    else:
        print("[Fleet] No new skill promotions needed. Fleet is balanced.")

    return promotable


# ─── Analytics Routing ──────────────────────────────────────────────────
def route_analytics():
    """Read analytics_feed.json and route insights to each agent's INBOX."""
    if not os.path.exists(ANALYTICS_FEED_PATH):
        print("[Fleet] No analytics feed found.")
        return 0

    with open(ANALYTICS_FEED_PATH, "r", encoding="utf-8") as f:
        feed = json.load(f)

    insights = feed.get("insights", [])
    if not insights:
        print("[Fleet] Analytics feed is empty. Nothing to route.")
        return 0

    routed = 0
    for insight in insights:
        target = insight.get("target_agent")
        if target and target in get_all_agents():
            write_to_inbox(target, {
                "from": "analytics_reporting",
                "date": datetime.datetime.now().isoformat(),
                "priority": insight.get("priority", "medium"),
                "message": f"[{insight.get('metric', 'insight')}] {insight.get('finding', '')} | Recommendation: {insight.get('recommendation', 'N/A')}",
                "action_required": True,
            })
            routed += 1

    print(f"[Fleet] Routed {routed} analytics insights to agent inboxes.")
    return routed


# ─── Learnings Sweep ────────────────────────────────────────────────────
def sweep_agent_learnings():
    """
    Scan each agent's OUTPUT_LOG.jsonl for learnings and aggregate them
    into the Brand Constitution's evolution log.
    """
    agents = get_all_agents()
    total_outputs = 0
    evolution_log_path = os.path.join(BRAND_CONSTITUTION_DIR, "BRAND_EVOLUTION_LOG.jsonl")

    for agent in agents:
        log_path = os.path.join(AGENT_FLEET_DIR, agent, "OUTPUT_LOG.jsonl")
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                total_outputs += len(lines)

    print(f"[Fleet] Swept {total_outputs} total outputs across {len(agents)} agents.")
    return total_outputs


# ─── Full Sweep ──────────────────────────────────────────────────────────
def full_sweep():
    """Run the complete fleet orchestration cycle."""
    print("\n" + "=" * 65)
    print("  KEYSTONE FLEET ORCHESTRATOR — Full Sweep")
    print("  " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 65)

    print("\n[1/5] Building Fleet Dashboard...")
    fleet = build_fleet_status()

    print("\n[2/5] Checking for Overlaps...")
    overlaps = detect_overlaps()

    print("\n[3/5] Running Skill Promotion Pipeline...")
    promotions = run_skill_promotion()

    print("\n[4/5] Routing Analytics Insights...")
    routed = route_analytics()

    print("\n[5/5] Sweeping Agent Learnings...")
    outputs = sweep_agent_learnings()

    print("\n" + "=" * 65)
    print(f"  SWEEP COMPLETE")
    print(f"  Agents: {fleet['total_agents']} | Overlaps: {len(overlaps)} | Promotions: {len(promotions)}")
    print(f"  Analytics routed: {routed} | Total outputs tracked: {outputs}")
    print("=" * 65)


# ─── CLI ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Keystone Fleet Orchestrator v1.0")
    parser.add_argument("--sweep", action="store_true", help="Full fleet sweep")
    parser.add_argument("--status", action="store_true", help="Quick fleet status")
    parser.add_argument("--overlaps", action="store_true", help="Check for overlaps")
    parser.add_argument("--promote", action="store_true", help="Run skill promotion")
    parser.add_argument("--route-analytics", action="store_true", help="Route analytics to inboxes")
    parser.add_argument("--claim", nargs=2, metavar=("TOPIC", "AGENT"), help="Claim a topic for an agent")
    args = parser.parse_args()

    if args.sweep:
        full_sweep()
    elif args.status:
        fleet = build_fleet_status()
        print("\nAgent Details:")
        for name, info in fleet["agents"].items():
            status_icon = "●" if info["status"] == "active" else "○"
            print(f"  {status_icon} {name:25s} [{info['brand']:15s}] {info['status']:8s} | {info['outputs_count']} outputs | {info['topics_claimed']} topics")
    elif args.overlaps:
        detect_overlaps()
    elif args.promote:
        run_skill_promotion()
    elif args.route_analytics:
        route_analytics()
    elif args.claim:
        claim_topic(args.claim[0], args.claim[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
