#!/usr/bin/env python3
"""
Keystone Dynamic Skill Compiler & Hot-Reloader
Automates the process of generating new skills, running AST validation checks,
running test fixtures inside the sandbox, committing to Git on success,
and hot-reloading the multiplexer to register the new skills as MCP tools.
"""

import os
import sys
import json
import argparse
import subprocess
from typing import Dict, Any, List

# Setup absolute paths
PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
SELF_EVOLUTION = os.path.join(PROJECT_ROOT, "self_evolution.py")

def compile_and_deploy_skill(name: str, description: str, code: str, fixtures: List[Dict[str, Any]]) -> bool:
    print("====================================================")
    print(f"Sovereign Skill Compiler: Deploying '{name}'")
    print("====================================================")
    
    # Imports inside function to avoid import conflicts
    sys.path.insert(0, PROJECT_ROOT)
    try:
        from self_evolution import SovereignSelfEvolution
    except ImportError as e:
        print(f"Error importing SovereignSelfEvolution: {e}")
        return False
        
    evolution_engine = SovereignSelfEvolution()
    
    # 1. Synthesize candidate script code
    # We ensure the script has proper type hints and comments
    formatted_code = f'"""\nEvolved Dynamic Skill: {name}\nDescription: {description}\n"""\n\n' + code.strip() + "\n"
    
    print(f"Compiled candidate code for module '{name}' ({len(formatted_code)} bytes).")
    
    # 2. Extract function name from code using simple parsing
    # Typically, we search for the first 'def <name>(' matching block
    import re
    match = re.search(r"def\s+([a-zA-Z0-9_]+)\(", code)
    if not match:
        print("Error: No function definition found in candidate code.")
        return False
    function_name = match.group(1)
    print(f"Detected primary entrypoint function: '{function_name}'")
    
    # 3. Run full sandboxed evolution cycle: AST -> sandbox -> test fixtures -> hot-reload -> Git
    success = evolution_engine.run_evolution_cycle(
        module_name=name,
        function_name=function_name,
        candidate_code=formatted_code,
        test_fixtures=fixtures
    )
    
    if success:
        print("\nSUCCESS: Skill validated, deployed, and hot-reloaded into MCP Multiplexer!")
        print(f"Dynamic Tool Name: dynamic_{name}_{function_name}")
    else:
        print("\nFAILURE: Skill did not pass safety or validation checks. Rollback completed.")
        
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keystone Sovereign Skill Compiler")
    parser.add_argument("--name", type=str, required=True, help="Filename of the dynamic skill (e.g. tax_utils)")
    parser.add_argument("--desc", type=str, required=True, help="Description of the dynamic skill functionality")
    parser.add_argument("--code-file", type=str, required=True, help="Path to Python file containing raw skill code")
    parser.add_argument("--fixtures-file", type=str, required=True, help="Path to JSON file containing test fixtures")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.code_file):
        print(f"Error: Code file not found: {args.code_file}")
        sys.exit(1)
        
    if not os.path.exists(args.fixtures_file):
        print(f"Error: Fixtures file not found: {args.fixtures_file}")
        sys.exit(1)
        
    with open(args.code_file, "r", encoding="utf-8") as f:
        skill_code = f.read()
        
    with open(args.fixtures_file, "r", encoding="utf-8") as f:
        skill_fixtures = json.load(f)
        
    result = compile_and_deploy_skill(
        name=args.name,
        description=args.desc,
        code=skill_code,
        fixtures=skill_fixtures
    )
    sys.exit(0 if result else 1)
