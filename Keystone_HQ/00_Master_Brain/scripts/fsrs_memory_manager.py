import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Ensure the library is installed
try:
    from fsrs import Scheduler, Card, Rating, ReviewLog
except ImportError:
    print("[Error] FSRS library is not installed. Run 'pip install fsrs' first.", file=sys.stderr)
    sys.exit(1)

# Ensure sys.stdout handles UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Setup paths
WORKSPACE_ROOT = Path(r"C:\Users\Curtis\New folder\construction-website")
MASTER_BRAIN = WORKSPACE_ROOT / "Keystone_HQ" / "00_Master_Brain"
LEARNINGS = MASTER_BRAIN / ".learnings"
CARDS_FILE = LEARNINGS / "fsrs_cards.json"
CORRECTION_JOURNAL = LEARNINGS / "correction_journal.json"

class AgentRule:
    """
    Represents a rule coupled with its FSRS card state.
    """
    def __init__(self, rule_id: str, content: str, card: Optional[Card] = None, status: str = "active"):
        self.rule_id = rule_id
        self.content = content
        self.card = card if card else Card()
        self.status = status  # "active" or "pruned"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "content": self.content,
            "card_state": self.card.to_dict(),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentRule':
        card = Card.from_dict(data["card_state"])
        return cls(
            rule_id=data["rule_id"],
            content=data["content"],
            card=card,
            status=data.get("status", "active")
        )

class FSRSMemoryManager:
    """
    Manages the FSRS-based memory decay for agent rules.
    """
    def __init__(self, target_retention: float = 0.90):
        # Configure the scheduler for programmatic rules
        self.scheduler = Scheduler(
            desired_retention=target_retention,
            enable_fuzzing=False,  # Enforce determinism
            learning_steps=(),     # Skip biological short-term steps
            relearning_steps=(),   # Skip biological relearning steps
            maximum_interval=365   # Cap at 1 year
        )
        self.rules: Dict[str, AgentRule] = {}
        self.review_logs: List[Dict[str, Any]] = []
        self.load_state()

    def load_state(self) -> None:
        if not CARDS_FILE.exists():
            self.rules = {}
            self.review_logs = []
            return
        try:
            with open(CARDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.rules = {
                k: AgentRule.from_dict(v) for k, v in data.get("rules", {}).items()
            }
            self.review_logs = data.get("review_logs", [])
        except Exception as e:
            print(f"[Error] Failed to load FSRS cards: {e}", file=sys.stderr)
            self.rules = {}
            self.review_logs = []

    def save_state(self) -> None:
        try:
            os.makedirs(CARDS_FILE.parent, exist_ok=True)
            data = {
                "rules": {k: v.to_dict() for k, v in self.rules.items()},
                "review_logs": self.review_logs
            }
            with open(CARDS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Error] Failed to save FSRS cards: {e}", file=sys.stderr)

    def add_rule(self, rule_id: str, content: str) -> bool:
        if rule_id in self.rules:
            # Rule already exists, update content if changed
            self.rules[rule_id].content = content
            return False
        self.rules[rule_id] = AgentRule(rule_id, content)
        self.save_state()
        return True

    def record_review(self, rule_id: str, rating_val: int) -> Optional[Tuple[Card, ReviewLog]]:
        if rule_id not in self.rules:
            print(f"[Error] Rule {rule_id} not found in store.", file=sys.stderr)
            return None

        # Map rating value to Rating enum
        rating_map = {
            1: Rating.Again,
            2: Rating.Hard,
            3: Rating.Good,
            4: Rating.Easy
        }
        rating = rating_map.get(rating_val, Rating.Good)
        rule = self.rules[rule_id]
        now = datetime.now(timezone.utc)

        # Py-FSRS review_card returns (updated_card, review_log)
        updated_card, review_log = self.scheduler.review_card(rule.card, rating, now)
        rule.card = updated_card
        
        # Save review log
        log_entry = {
            "rule_id": rule_id,
            "rating": rating_val,
            "timestamp": now.isoformat(),
            "card_state_before": rule.card.to_dict()  # Save snapshot
        }
        self.review_logs.append(log_entry)
        
        # Reactivate rule if reviewed successfully (Rating > Again)
        if rating_val > 1 and rule.status == "pruned":
            rule.status = "active"
            print(f"Reactivated rule {rule_id} due to positive review.")

        self.save_state()
        return updated_card, review_log

    def prune_rules(self, threshold: float = 0.5) -> List[str]:
        now = datetime.now(timezone.utc)
        pruned_ids = []
        for rule_id, rule in self.rules.items():
            if rule.status == "active":
                r_score = self.scheduler.get_card_retrievability(rule.card, now)
                # If card has not been reviewed, retrievability is 0 or None; initially let it be active
                if rule.card.last_review is None:
                    continue
                if r_score is not None and r_score < threshold:
                    rule.status = "pruned"
                    pruned_ids.append(rule_id)
        if pruned_ids:
            self.save_state()
        return pruned_ids

    def get_active_rules(self, threshold: float = 0.5) -> List[AgentRule]:
        now = datetime.now(timezone.utc)
        active_list = []
        for rule in self.rules.values():
            if rule.status == "active":
                if rule.card.last_review is None:
                    active_list.append(rule)
                    continue
                r_score = self.scheduler.get_card_retrievability(rule.card, now)
                if r_score is None or r_score >= threshold:
                    active_list.append(rule)
        return active_list

    def sync_from_correction_journal(self) -> int:
        """
        Scans correction_journal.json and adds any new prevention rules.
        """
        if not CORRECTION_JOURNAL.exists():
            return 0
        try:
            with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
                journal = json.load(f)
            added_count = 0
            for entry in journal:
                rule_id = entry.get("id")
                # Fallback to creating a hash-based ID if missing
                if not rule_id:
                    import hashlib
                    err_txt = entry.get("error", "")
                    rule_id = "CJ-" + hashlib.md5(err_txt.encode('utf-8')).hexdigest()[:8]
                
                content = entry.get("prevention_rule") or entry.get("prevention")
                if content:
                    if self.add_rule(rule_id, content):
                        added_count += 1
            return added_count
        except Exception as e:
            print(f"[Error] Failed to sync from correction journal: {e}", file=sys.stderr)
            return 0

def main():
    import argparse
    parser = argparse.ArgumentParser(description="FSRS-based Agent Memory Manager CLI")
    parser.add_argument("--list", action="store_true", help="List all rules and their FSRS DSR metrics")
    parser.add_argument("--add", action="store_true", help="Add a new rule")
    parser.add_argument("--id", type=str, help="Rule ID")
    parser.add_argument("--content", type=str, help="Rule content / text")
    parser.add_argument("--review", action="store_true", help="Record a review hit")
    parser.add_argument("--rating", type=int, choices=[1, 2, 3, 4], help="Rating: 1=Again, 2=Hard, 3=Good, 4=Easy")
    parser.add_argument("--prune", action="store_true", help="Run the pruning cycle")
    parser.add_argument("--threshold", type=float, default=0.5, help="Retrievability threshold (default: 0.5)")
    parser.add_argument("--sync-journal", action="store_true", help="Sync new rules from the correction journal")
    
    args = parser.parse_args()
    manager = FSRSMemoryManager()

    if args.list:
        now = datetime.now(timezone.utc)
        print(f"\n--- FSRS Rules State (Current Time: {now.isoformat()}) ---")
        print(f"{'Rule ID':<25} {'Stability':<10} {'Difficulty':<10} {'Retrievability':<15} {'Status':<8}")
        print("-" * 75)
        for rule_id, rule in sorted(manager.rules.items()):
            r_score = manager.scheduler.get_card_retrievability(rule.card, now) if rule.card.last_review else 1.0
            r_str = f"{r_score:.4f}" if r_score is not None else "N/A"
            stab_str = f"{rule.card.stability:.4f}" if rule.card.stability is not None else "N/A"
            diff_str = f"{rule.card.difficulty:.4f}" if rule.card.difficulty is not None else "N/A"
            print(f"{rule_id:<25} {stab_str:<10} {diff_str:<10} {r_str:<15} {rule.status:<8}")
        print()
        return

    if args.add:
        if not args.id or not args.content:
            print("Error: --id and --content are required when adding a rule.", file=sys.stderr)
            sys.exit(1)
        added = manager.add_rule(args.id, args.content)
        if added:
            print(f"Added new rule: {args.id}")
        else:
            print(f"Updated content of existing rule: {args.id}")
        return

    if args.review:
        if not args.id or not args.rating:
            print("Error: --id and --rating are required when reviewing a rule.", file=sys.stderr)
            sys.exit(1)
        res = manager.record_review(args.id, args.rating)
        if res:
            card, log = res
            print(f"Reviewed rule {args.id} successfully.")
            print(f"  Stability:  {card.stability:.4f}")
            print(f"  Difficulty: {card.difficulty:.4f}")
            print(f"  Due date:   {card.due.isoformat()}")
        return

    if args.prune:
        pruned = manager.prune_rules(args.threshold)
        print(f"Pruning complete. Rules pruned: {len(pruned)}")
        for pid in pruned:
            print(f"  - {pid}")
        return

    if args.sync_journal:
        added = manager.sync_from_correction_journal()
        print(f"Synced from correction journal. Rules added: {added}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
