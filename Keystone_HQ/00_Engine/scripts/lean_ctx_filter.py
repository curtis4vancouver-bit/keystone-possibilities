#!/usr/bin/env python3
"""
Keystone Sovereign - lean-ctx Local Terminal Output Compressor.
Compresses verbose command-line executions, test logs, and build loops, 
reducing context window token consumption by up to 99%.
Preserves critical warning, failure, and traceback states verbatim.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List

# Target Workspace Roots
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
TRANSCRIPTS_DIR = ROOT_DIR / "Transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


class LeanCortexFilter:
    def __init__(self):
        # Patterns to preserve completely verbatim (errors, tracebacks, warnings)
        self.preserve_patterns = [
            r"error", r"warning", r"fail", r"exception", r"critical", 
            r"traceback", r"line \d+", r"syntaxerror", r"assertionerror",
            r"permissionerror", r"not found", r"denied", r"halt"
        ]
        self.compiled_preserve = [re.compile(p, re.IGNORECASE) for p in self.preserve_patterns]
        
        # Patterns representing repetitive success loops
        self.success_patterns = [
            r"\.\.\.\s*ok", r"\.\.\.\s*passed", r"\.\.\.\s*success", 
            r"test\s+\w+\s*passed", r"fixture\s+\d+\s*ok", r"syncing\s+\w+\s*\.\.\.\s*complete"
        ]
        self.compiled_success = [re.compile(p, re.IGNORECASE) for p in self.success_patterns]

    def is_critical(self, line: str) -> bool:
        """Determines if a line contains critical warning or error telemetry."""
        return any(rx.search(line) for rx in self.compiled_preserve)

    def is_repetitive_success(self, line: str) -> bool:
        """Determines if a line is a routine success log eligible for compression."""
        return any(rx.search(line) for rx in self.compiled_success)

    def compress_terminal_output(self, raw_output: str) -> str:
        """
        Parses raw CLI output and compresses redundant blocks.
        Collapses repetitive successful test logs and strips loading animations.
        """
        lines = raw_output.splitlines()
        compressed_lines = []
        success_streak = 0
        
        for line in lines:
            line_strip = line.strip()
            if not line_strip:
                continue

            # Strip spinners and loading bar noise (e.g. [===/===>])
            line_strip = re.sub(r'[\b\r]', '', line_strip)  # Clear backspaces/carriage returns
            line_strip = re.sub(r'\[[=#>-]+\]\s*\d+%', '', line_strip) # Clear loading bars
            line_strip = re.sub(r'[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]\s*Loading.*', '', line_strip) # Clear loading spinners

            # Evaluate content category
            if self.is_critical(line_strip):
                # Flush success streaks first
                if success_streak > 0:
                    compressed_lines.append(f"[Lean Cortex: {success_streak} routine success cycles compacted to 1 line]")
                    success_streak = 0
                compressed_lines.append(line_strip)
                
            elif self.is_repetitive_success(line_strip):
                success_streak += 1
                
            else:
                # Flush success streaks first
                if success_streak > 0:
                    compressed_lines.append(f"[Lean Cortex: {success_streak} routine success cycles compacted to 1 line]")
                    success_streak = 0
                compressed_lines.append(line_strip)

        # Final flush on stream termination
        if success_streak > 0:
            compressed_lines.append(f"[Lean Cortex: {success_streak} routine success cycles compacted to 1 line]")

        return "\n".join(compressed_lines)


def main():
    parser = argparse.ArgumentParser(description="lean-ctx context compressor for terminal logs.")
    parser.add_argument("--file", help="Path to a log file to compress.")
    parser.add_argument("--simulate-test-run", action="store_true", help="Runs a mock test-suite log compression to verify token savings.")
    
    args = parser.parse_args()
    cortex = LeanCortexFilter()

    if args.simulate_test_run:
        # Create a mock verbose output resembling 100+ unit test results
        mock_output = (
            "KEYSTONE UNIT TEST SUITE DEPLOYMENT\n"
            "Initializing environment fixtures...\n"
            "Testing Form Component: DiagnosticForm.tsx ... OK\n"
            "Testing Endpoint Integration: api/contact-api ... OK\n"
            "Testing Security Gate: path_traversal_check ... passed\n"
        )
        for i in range(1, 150):
            mock_output += f"Testing Subagent Thread: runner_instance_{i:03d} ... passed\n"
            
        mock_output += (
            "Testing Media Render: heygen_video_engine.py ... passed\n"
            "Testing Audio Compilation: multilingual_lexicon_skip ... FAIL\n"
            "AssertionError: phonetic XML tag was omitted by Multilingual v2\n"
            "Testing Complete: 153 passed, 1 failed, 0 ignored.\n"
        )
        
        compressed = cortex.compress_terminal_output(mock_output)
        
        # Calculate token savings estimation
        raw_char_count = len(mock_output)
        comp_char_count = len(compressed)
        savings_pct = (1.0 - (comp_char_count / raw_char_count)) * 100
        
        print("=" * 70)
        print("LEAN CORTEX TERMINAL COMPRESSION REPORT")
        print("=" * 70)
        print(f"Original characters:   {raw_char_count}")
        print(f"Compressed characters: {comp_char_count}")
        print(f"Dynamic Token Savings: {savings_pct:.2f}%")
        print("-" * 70)
        print("COMPRESSED OUTPUT STREAM:")
        print("-" * 70)
        print(compressed)
        print("=" * 70)
        
    elif args.file:
        log_path = Path(args.file)
        if not log_path.exists():
            print(f"Error: Log file not found at: {log_path}")
            sys.exit(1)
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(cortex.compress_terminal_output(content))
        
    else:
        # Standard stdio pipeline filter
        if sys.stdin.isatty():
            print("Usage: pipe raw console logs to this script, e.g.: python run_tests.py | python scripts/lean_ctx_filter.py")
        else:
            raw_input = sys.stdin.read()
            print(cortex.compress_terminal_output(raw_input))


if __name__ == "__main__":
    main()
