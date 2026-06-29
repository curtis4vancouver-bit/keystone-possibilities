import os
import sys
import time
import shutil
import threading
import unittest
from pathlib import Path

# Force UTF-8 output on Windows to handle emojis in logs and print statements
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Fix paths to allow core imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.brain_init import init_brain_transplant
from core.state_store import StateStore
from core.skill_generator import SkillGenerator
from core.conversation_compressor import ConversationCompressor
from core.memory_manager import MemoryManager
from core.self_knowledge import SelfKnowledgeManager
from core.self_healer import SelfHealer
from core.error_classifier import ErrorClassifier, ErrorType

# Dynamic paths for test run
TEST_DB_PATH = ROOT_DIR / "scratch" / "test_state.db"
TEST_SKILLS_DIR = ROOT_DIR / "scratch" / "test_skills"

class TestBrainTransplant(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Clean up existing test dirs
        if TEST_DB_PATH.exists():
            try:
                TEST_DB_PATH.unlink()
                # Clean WAL files
                for f in TEST_DB_PATH.parent.glob("test_state.db*"):
                    f.unlink()
            except Exception:
                pass
        if TEST_SKILLS_DIR.exists():
            shutil.rmtree(TEST_SKILLS_DIR)
            
        TEST_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Instantiate StateStore
        cls.store = StateStore(str(TEST_DB_PATH))
        cls.skill_gen = SkillGenerator(str(TEST_SKILLS_DIR))
        cls.compressor = ConversationCompressor(cls.store)
        cls.memory_mgr = MemoryManager(cls.store)
        cls.self_knowledge = SelfKnowledgeManager(cls.store)
        cls.healer = SelfHealer(cls.store, cls.compressor)

    def test_01_state_store_sessions_and_messages(self):
        """Verifies session and message creation, and FTS5 search."""
        session_id = "test_session_001"
        self.store.create_session(
            session_id=session_id,
            source="test_runner",
            model="gemini-3.5-flash",
            system_prompt="You are a verification agent."
        )
        
        # Verify session is created
        sessions = self.store.get_recent_sessions(limit=10)
        self.assertTrue(any(s["id"] == session_id for s in sessions))
        
        # Add messages
        msg_id1 = self.store.add_message(session_id, "user", "I am installing a sauna in West Vancouver.")
        msg_id2 = self.store.add_message(session_id, "assistant", "sauna installation requires building permits.")
        
        self.assertIsNotNone(msg_id1)
        self.assertIsNotNone(msg_id2)

        # FTS5 search matching
        matches = self.store.search_messages("sauna")
        self.assertTrue(len(matches) >= 1)
        self.assertTrue(any("sauna" in m["content"] for m in matches))

    def test_02_write_contention_concurrency(self):
        """Verifies concurrent threads can write safely via locks and retry loops."""
        errors = []
        
        def writer_thread(tid: int):
            try:
                for i in range(10):
                    self.store.add_message("test_session_001", "user", f"Thread {tid} write {i}")
                    time.sleep(0.01)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer_thread, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Concurrency errors: {errors}")

    def test_03_skill_generator_and_validator(self):
        """Verifies skill validator rejects malformed structure and curates properly."""
        valid_skill = """---
name: test-sauna-installer
description: "Handles sauna dimensions and electrical requirements."
version: 1.0.0
author: Verification Suite
license: MIT
platforms: [windows]
---
# Sauna Installation Skill
Ensure electrical panel supports 240V heaters.
"""
        
        invalid_skill = """---
name: Invalid_Name_With_Capitals
description: "Broken name check"
---
# Content
"""

        # Validation checks
        is_valid, err = self.skill_gen.validate_skill(valid_skill)
        self.assertTrue(is_valid, f"Valid skill failed validation: {err}")

        is_invalid, err = self.skill_gen.validate_skill(invalid_skill)
        self.assertFalse(is_invalid)
        self.assertIn("invalid", err.lower())

        # Write skill atomically
        filepath = self.skill_gen.write_skill(valid_skill)
        self.assertTrue(os.path.exists(filepath))

        # Check usage ledger
        self.skill_gen.track_use("test-sauna-installer", is_view=True)
        self.skill_gen.track_use("test-sauna-installer", is_view=False)
        self.assertEqual(self.skill_gen.usage_data["test-sauna-installer"]["view_count"], 1)
        self.assertEqual(self.skill_gen.usage_data["test-sauna-installer"]["use_count"], 1)

    def test_04_conversation_compression(self):
        """Verifies Tier 1 pruning and Tier 2 middle turn summary compactions."""
        verbose_stdout = "Execution output:\n" + "\n".join(f"line {i}: testing data output stream" for i in range(100))
        pruned = self.compressor.prune_tool_output("run_command", verbose_stdout)
        self.assertIn("Pruned Stdio", pruned)
        self.assertTrue(len(pruned) < len(verbose_stdout))

        # Simulate large message history
        messages = [
            {"role": "system", "content": "Instructions"},
            {"role": "user", "content": "Query 1"},
            {"role": "assistant", "content": "Response 1"},
            {"role": "user", "content": "Query 2"},
            {"role": "assistant", "content": "Response 2"},
            {"role": "user", "content": "Query 3"},
            {"role": "assistant", "content": "Response 3"},
            {"role": "user", "content": "Query 4"},
            {"role": "assistant", "content": "Response 4"},
            {"role": "user", "content": "Query 5"},
            {"role": "assistant", "content": "Response 5"}
        ]
        
        compacted = self.compressor.compress_tier2_and_3(messages)
        self.assertTrue(len(compacted) < len(messages))
        self.assertEqual(compacted[0]["content"], "Instructions")
        self.assertEqual(compacted[-1]["content"], "Response 5")
        self.assertTrue(any("[CONTEXT COMPACTION" in m.get("content", "") for m in compacted))

    def test_05_self_healing_database_repair(self):
        """Verifies database self-repair can rebuild virtual indexes."""
        # Intentionally break FTS virtual table triggers or drop virtual table
        self.store._execute_write("DROP TABLE IF EXISTS messages_fts;")
        
        # Test self-healer/repair trigger
        self.store.repair_database()
        
        # Verify FTS index works again
        msg_id = self.store.add_message("test_session_001", "user", "repaired sauna heating system")
        matches = self.store.search_messages("repaired")
        self.assertTrue(len(matches) >= 1)

    def test_06_self_knowledge_system(self):
        """Verifies AI self-modeling updates and dynamic rules generation."""
        self.self_knowledge.record_self_correction(
            tendency="lazy subagent delegation",
            correction="always run tasks directly in current conversation",
            context="google flow"
        )
        
        prompt = self.self_knowledge.get_rules_prompt()
        self.assertIn("self-knowledge-directives", prompt)
        self.assertIn("lazy subagent delegation", prompt)
        self.assertIn("always run tasks directly", prompt)

def main():
    print("=== RUNNING AUTOMATED BRAIN TRANSPLANT TEST SUITE ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBrainTransplant)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Clean up test directories
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
            for f in TEST_DB_PATH.parent.glob("test_state.db*"):
                f.unlink()
        except Exception:
            pass
    if TEST_SKILLS_DIR.exists():
        shutil.rmtree(TEST_SKILLS_DIR)
        
    if result.wasSuccessful():
        print("\n✅ Verification tests completed successfully. All components operational!")
        sys.exit(0)
    else:
        print("\n❌ Verification tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
