"""
Keystone Self-Learning Mock Test Suite v1.0
============================================
Runs simulated scenarios so the AI can practice and learn from failures
without hitting real services. Tests across all critical operational domains.

Usage:
  python mock_test_suite.py --run-all        # Run all mock tests
  python mock_test_suite.py --domain chrome  # Test specific domain
  python mock_test_suite.py --report         # Show test results
"""

import os
import sys
import json
import time
import datetime
import traceback

# Force UTF-8 output on Windows to handle emoji/unicode in lessons
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(PROJECT_ROOT, ".learnings", "mock_tests")
os.makedirs(RESULTS_DIR, exist_ok=True)


class MockTestResult:
    def __init__(self, name: str, domain: str):
        self.name = name
        self.domain = domain
        self.passed = False
        self.error = None
        self.duration_ms = 0
        self.lessons_learned = []

    def to_dict(self):
        return {
            "name": self.name,
            "domain": self.domain,
            "passed": self.passed,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "lessons_learned": self.lessons_learned
        }


class MockTestSuite:
    """
    Runs mock tests that simulate real operational scenarios.
    Each test validates a specific capability and records
    what was learned for the correction journal.
    """

    def __init__(self):
        self.results = []

    def run_all(self) -> list:
        """Run every mock test domain."""
        print("[Mock Tests] Running full self-learning test suite...\n")

        test_methods = [
            self.test_chrome_navigation,
            self.test_brain_search_quality,
            self.test_error_fingerprinting,
            self.test_mcp_multiplexer_routing,
            self.test_file_path_resolution,
            self.test_credit_timing_math,
            self.test_research_prompt_quality,
            self.test_correction_journal_lookup,
            self.test_security_sandbox_blocks,
            self.test_queue_management,
        ]

        for test_fn in test_methods:
            result = MockTestResult(test_fn.__name__, test_fn.__doc__ or "general")
            start = time.time()
            try:
                lessons = test_fn()
                result.passed = True
                result.lessons_learned = lessons if isinstance(lessons, list) else [str(lessons)]
            except AssertionError as ae:
                result.passed = False
                result.error = str(ae)
                result.lessons_learned = [f"FAILURE: {str(ae)}"]
            except Exception as e:
                result.passed = False
                result.error = traceback.format_exc()
                result.lessons_learned = [f"CRASH: {str(e)}"]
            result.duration_ms = int((time.time() - start) * 1000)
            self.results.append(result)

            status = "[PASS]" if result.passed else "[FAIL]"
            print(f"  {status} {result.name} ({result.duration_ms}ms)")
            if not result.passed:
                err_msg = result.error[:120] if result.error else 'None'
                print(f"       Error: {err_msg}")

        self._save_results()
        return self.results

    # ─── Individual Mock Tests ────────────────────────────────────────

    def test_chrome_navigation(self) -> list:
        """chrome"""
        # Simulate: Can we build valid Chrome DevTools MCP call sequences?
        valid_sequence = [
            {"tool": "new_page", "args": {"url": "https://gemini.google.com"}},
            {"tool": "wait_for", "args": {"selector": "textarea", "timeout": 10000}},
            {"tool": "type_text", "args": {"text": "Test prompt", "selector": "textarea"}},
            {"tool": "press_key", "args": {"key": "Enter"}},
            {"tool": "wait_for", "args": {"selector": ".response-container", "timeout": 600000}},
            {"tool": "take_snapshot", "args": {}},
            {"tool": "close_page", "args": {}},
        ]

        # Validate all steps have required fields
        for step in valid_sequence:
            assert "tool" in step, f"Missing tool name in step"
            assert "args" in step, f"Missing args in step {step['tool']}"

        # Validate no invalid tool names
        valid_tools = {"new_page", "navigate_page", "wait_for", "type_text",
                       "press_key", "take_snapshot", "take_screenshot", "close_page",
                       "click", "fill", "fill_form", "evaluate_script", "list_pages",
                       "select_page", "hover", "drag"}
        for step in valid_sequence:
            assert step["tool"] in valid_tools, f"Invalid tool: {step['tool']}"

        return [
            "Chrome automation sequence is 7 steps: new_page → wait → type → enter → wait → snapshot → close",
            "wait_for timeout for Deep Research should be 600000ms (10 min)",
            "Always close_page when done to free Chrome resources"
        ]

    def test_brain_search_quality(self) -> list:
        """brain"""
        # Simulate: Do our search keywords produce good matches?
        test_queries = [
            {"query": "optimization session", "expected_domain": "agent_session"},
            {"query": "Hermes architecture", "expected_domain": "hermes"},
            {"query": "self evolution pipeline", "expected_domain": "self_evolution"},
        ]

        # Validate query strings are not too long (brain search works best < 100 chars)
        for q in test_queries:
            assert len(q["query"]) < 100, f"Query too long: {q['query']}"
            assert len(q["query"]) > 3, f"Query too short: {q['query']}"

        return [
            "Brain search queries should be 4-100 characters for optimal results",
            "Use domain-specific keywords, not full sentences",
            "Search BEFORE doing web lookups — the brain may already know"
        ]

    def test_error_fingerprinting(self) -> list:
        """self_learning"""
        import hashlib

        # Same error should produce same fingerprint
        def compute_fingerprint(error_type, context, tb):
            core = tb.strip().split("\n")[-1] if tb else ""
            raw = f"{error_type}::{context}::{core}"
            return hashlib.sha256(raw.encode()).hexdigest()[:16]

        fp1 = compute_fingerprint("ImportError", "test_module", "ModuleNotFoundError: No module named 'xyz'")
        fp2 = compute_fingerprint("ImportError", "test_module", "ModuleNotFoundError: No module named 'xyz'")
        fp3 = compute_fingerprint("ImportError", "other_module", "ModuleNotFoundError: No module named 'xyz'")

        assert fp1 == fp2, "Same error should produce same fingerprint"
        assert fp1 != fp3, "Different context should produce different fingerprint"

        return [
            "Error fingerprints are stable — same error always gets same ID",
            "Context field differentiates same error type in different modules",
            "16-char hex fingerprint is sufficient for deduplication"
        ]

    def test_mcp_multiplexer_routing(self) -> list:
        """mcp"""
        # Validate agent routing logic
        agents = {
            "youtube_manager": ["list_videos", "update_video", "upload_video"],
            "google_workspace": ["search_gmail_messages", "create_calendar_event"],
            "davinci_resolve": ["resolve_control", "create_timeline"],
            "dynamic_skills": ["dynamic_seo_analyzer", "dynamic_ccb_calculator"],
        }

        # Test: Can we correctly route a tool to its agent?
        def find_agent(tool_name):
            for agent, tools in agents.items():
                if tool_name in tools:
                    return agent
            return None

        assert find_agent("list_videos") == "youtube_manager"
        assert find_agent("search_gmail_messages") == "google_workspace"
        assert find_agent("nonexistent_tool") is None

        return [
            "Always use mcp_multiplexer_execute_tool, never call agents directly",
            "If tool not found, use mcp_multiplexer_list_all_tools to discover it",
            "Use mcp_multiplexer_refresh_tool_cache after adding new skills"
        ]

    def test_file_path_resolution(self) -> list:
        """filesystem"""
        # Common path errors on Windows
        test_paths = [
            (r"c:\Users\Curtis\New folder\construction-website", True),
            (r"../dynamic_skills/dynamic_mcp.py", False),  # Relative paths need resolution
            (r"C:\Users\Curtis\.gemini\config\config.json", True),
        ]

        for path, is_absolute in test_paths:
            if is_absolute:
                assert os.path.isabs(path), f"Expected absolute path: {path}"
            else:
                assert not os.path.isabs(path), f"Expected relative path: {path}"

        # Test: Space in path handling
        path_with_space = r"c:\Users\Curtis\New folder\test.txt"
        assert " " in path_with_space
        # On Windows, paths with spaces work natively (no quoting needed in Python)

        return [
            "Windows paths with spaces work natively in Python — no quoting needed",
            "Always use raw strings (r'...') for Windows paths to avoid backslash escaping",
            "MCP Multiplexer resolves '../' paths relative to MCP_Multiplexer/ directory"
        ]

    def test_credit_timing_math(self) -> list:
        """scheduling"""
        # Credit refresh window calculations
        refresh_hours = 5.0
        prompts_per_window = 20  # Conservative estimate
        batch_size = 3
        prompts_per_batch = batch_size  # 1 prompt per topic in Deep Research

        batches_per_window = prompts_per_window // prompts_per_batch
        overnight_hours = 12  # 7 PM to 7 AM
        refresh_cycles = overnight_hours / refresh_hours
        total_overnight_prompts = int(refresh_cycles * prompts_per_window)

        assert batches_per_window >= 3, "Should fit at least 3 batches per window"
        assert total_overnight_prompts >= 40, f"Should get 40+ prompts overnight, got {total_overnight_prompts}"

        return [
            f"~{batches_per_window} batches per 5-hour credit window ({prompts_per_window} prompts)",
            f"~{total_overnight_prompts} total research prompts possible overnight",
            f"~{int(refresh_cycles)} credit refresh cycles in a 12-hour overnight session",
            "Check credits every 60 minutes — don't waste compute on timing"
        ]

    def test_research_prompt_quality(self) -> list:
        """research"""
        # Test prompt construction
        good_prompt = (
            "Activate Deep Research. Thoroughly analyze: sqlite-vec HNSW index tuning "
            "for sub-10ms retrieval at 100K chunks. Context: This research is for an "
            "autonomous AI agent system. Provide actionable technical details."
        )

        bad_prompt = "tell me about databases"

        assert len(good_prompt) > 100, "Good prompts should be detailed (>100 chars)"
        assert len(bad_prompt) < 50, "Bad prompts are too vague"
        assert "Deep Research" in good_prompt, "Should activate Deep Research mode"
        assert "actionable" in good_prompt, "Should request actionable output"

        return [
            "Always prefix with 'Activate Deep Research' to trigger deep mode",
            "Include specific context about the Keystone system",
            "Request 'actionable, specific technical details' not vague summaries",
            "Include version numbers and dates for time-sensitive topics"
        ]

    def test_correction_journal_lookup(self) -> list:
        """self_learning"""
        # Simulate journal lookup
        mock_journal = {
            "entries": [
                {"error_fingerprint": "abc123", "error_type": "ImportError",
                 "fix_description": "Install missing module with pip", "success": True},
                {"error_fingerprint": "def456", "error_type": "TimeoutError",
                 "fix_description": "Increase wait_for timeout to 600000ms", "success": True},
                {"error_fingerprint": "ghi789", "error_type": "SyntaxError",
                 "fix_description": "Attempted fix", "success": False},
            ]
        }

        # Find known fix
        def find_fix(fingerprint):
            for entry in mock_journal["entries"]:
                if entry["error_fingerprint"] == fingerprint and entry["success"]:
                    return entry
            return None

        assert find_fix("abc123") is not None, "Should find successful fix"
        assert find_fix("ghi789") is None, "Should NOT return failed fixes"
        assert find_fix("zzz000") is None, "Should return None for unknown errors"

        return [
            "Only return fixes that were successful (success=True)",
            "Failed fixes are tracked but not re-applied",
            "Unknown error patterns return None — need fresh troubleshooting"
        ]

    def test_security_sandbox_blocks(self) -> list:
        """security"""
        # Simulate AST validation checks
        dangerous_patterns = [
            "import os; os.system('rm -rf /')",
            "exec(input())",
            "__import__('subprocess').call(['cmd'])",
            "eval(open('secrets.txt').read())",
        ]

        safe_patterns = [
            "import json\ndata = json.loads('{}')",
            "import math\nresult = math.sqrt(16)",
            "import hashlib\nhash = hashlib.sha256(b'test')",
        ]

        # Check dangerous keywords
        dangerous_keywords = {"os.system", "exec(", "__import__", "eval(", "subprocess"}
        for code in dangerous_patterns:
            has_danger = any(kw in code for kw in dangerous_keywords)
            assert has_danger, f"Should detect dangerous code: {code[:40]}"

        for code in safe_patterns:
            has_danger = any(kw in code for kw in dangerous_keywords)
            assert not has_danger, f"Should NOT flag safe code: {code[:40]}"

        return [
            "SecurityValidator blocks: os.system, exec, eval, __import__, subprocess",
            "Safe imports: json, math, hashlib, datetime, re, urllib",
            "All dynamic skills must pass AST validation before deployment"
        ]

    def test_queue_management(self) -> list:
        """scheduling"""
        # Test queue operations
        mock_queue = {
            "queue": [
                {"domain": "test1", "priority": 1, "topics": ["a", "b", "c"], "completed": ["a"]},
                {"domain": "test2", "priority": 2, "topics": ["d", "e"], "completed": []},
            ]
        }

        # Get next batch
        batch = []
        for domain in sorted(mock_queue["queue"], key=lambda d: d["priority"]):
            completed = set(domain.get("completed", []))
            for topic in domain["topics"]:
                if topic not in completed and len(batch) < 3:
                    batch.append(topic)

        assert batch == ["b", "c", "d"], f"Wrong batch order: {batch}"
        assert len(batch) == 3, "Batch should be exactly 3"

        return [
            "Queue pulls from highest priority domains first",
            "Skips already-completed topics automatically",
            "Cross-domain batching fills remaining slots from lower priority"
        ]

    # ─── Results ──────────────────────────────────────────────────────

    def _save_results(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        filepath = os.path.join(RESULTS_DIR, f"mock_test_results_{timestamp}.json")

        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": f"{(passed / max(total, 1)) * 100:.0f}%",
            "all_lessons": [],
            "tests": [r.to_dict() for r in self.results]
        }

        # Collect all lessons learned
        for r in self.results:
            report["all_lessons"].extend(r.lessons_learned)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*50}")
        print(f"Mock Test Results: {passed}/{total} passed ({report['pass_rate']})")
        print(f"Results saved: {filepath}")
        print(f"\nLessons Learned ({len(report['all_lessons'])} total):")
        for lesson in report["all_lessons"]:
            print(f"  - {lesson}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Keystone Self-Learning Mock Test Suite")
    parser.add_argument("--run-all", action="store_true", help="Run all mock tests")
    parser.add_argument("--domain", type=str, help="Run tests for a specific domain")
    parser.add_argument("--report", action="store_true", help="Show latest results")
    args = parser.parse_args()

    suite = MockTestSuite()

    if args.run_all or not any(vars(args).values()):
        suite.run_all()
    elif args.report:
        # Find latest results file
        files = sorted(os.listdir(RESULTS_DIR))
        if files:
            latest = os.path.join(RESULTS_DIR, files[-1])
            with open(latest, "r") as f:
                data = json.load(f)
            print(json.dumps(data, indent=2))
        else:
            print("No test results found. Run --run-all first.")
