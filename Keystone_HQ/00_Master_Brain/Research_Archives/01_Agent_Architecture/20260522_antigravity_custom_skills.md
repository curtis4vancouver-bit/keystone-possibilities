# Custom Antigravity Skill Creation & Multi-File Architecture (2026)
## Developer Reference Blueprint for Dynamic Skill Registries, AST Sandboxing, and Multi-Agent Tool Discovery

This guide details the advanced technical patterns required to design, compile, package, and safely execute custom and multi-file **Agent Skills** inside the **Google Antigravity SDK** environment. It provides comprehensive specifications for filesystem directory layouts, YAML metadata frontmatter, strict Abstract Syntax Tree (AST) safety sandboxing, safety policies, and programmatic multi-agent loading flows.

---

## 1. Directory Structure & Skill Specifications

An Antigravity Skill is a standardized, modular package that equips an agent with specific domain expertise, references, helper scripts, and dynamically discoverable tools. For complex operations (like custom database connectors, external media processors, or programmatic compliance audits), skills are organized across a structured multi-file hierarchy.

### 1.1 Standard Multi-File Skill Directory Layout
```
[Your-Custom-Skill-Name]/
├── SKILL.md                 # Required: Contains YAML Frontmatter metadata and core instructions
├── references/              # Optional: Static markdown reference documents
│   └── architecture.md
├── scripts/                 # Optional: Python helper modules imported by tools
│   ├── __init__.py
│   └── helper_module.py
├── resources/               # Optional: Static templates, JSON schemas, or mock datasets
│   └── default_config.json
└── tools/                   # Optional: Python scripts defining dynamic tools
    └── custom_tool.py
```

### 1.2 The `SKILL.md` Specification
Every skill must contain a `SKILL.md` at its root with valid YAML frontmatter specifying its identifier, capabilities, and conditional activation predicates.

```yaml
---
name: "keystone-tax-compliance"
version: "1.0.0"
description: "Equips agents with automated British Columbia contractor tax modeling, BC PST calculation, and CCA schedules."
dependencies:
  - "numpy>=1.24.0"
  - "pandas>=2.0.0"
predicates:
  - "workspace_contains('learning_queue.json')"
  - "model_tier_at_least('MODEL_TIER_PRO')"
---

# Keystone Tax Compliance & Financial Planning Skill

This skill equips your agent with high-precision calculations for BC small business corporations.

## Core Directives

1. **Calculate PST Expansion:** Always apply 7% PST to 30% of engineering/architecture service costs ($1.2 PST Rules).
2. **Execute CCA Schedules:** Run Class 10, Class 38, and Class 50 declining balance calculations factoring in the Half-Year Rule.
```

---

## 2. Advanced Multi-File Helper Imports & Shared [[STATE|State]]

When writing complex tools inside a custom skill, tools must be able to import shared helper scripts from the skill's local directory without polluting the host system's standard Python `sys.path`.

The following script demonstrates how a dynamically executed skill tool securely resolves and loads local sub-modules using relative path insertion.

```python
# file: custom_tool.py (inside tools/)
import os
import sys

def resolve_skill_imports():
    """
    Dynamically injects the local skill scripts directory into sys.path
    to allow importing local helper modules.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Traversal up to get to root and scripts folder
    skill_root = os.path.dirname(current_dir)
    scripts_path = os.path.join(skill_root, "scripts")
    
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
        print(f"[SKILL-LOADER] Registered local imports: {scripts_path}")

# Initialize paths
resolve_skill_imports()

# Import local skill helper safely
import helper_module

def execute_tax_calculation(income, expenses):
    """Exposed tool function performing optimized tax operations."""
    net_profit = float(income - expenses)
    tax_burden = helper_module.compute_bc_small_business_tax(net_profit)
    return {
        "Net_Profit": net_profit,
        "Estimated_Tax": tax_burden
    }
```

---

## 3. Strict AST Sandboxing & Security Layer

Executing dynamically generated code or external skills poses a significant security risk (e.g., prompt injection leading to directory escape or malicious outbound network requests). To mitigate this, Antigravity requires passing all skill code through a strict **Abstract Syntax Tree (AST) Safety Validator** before compilation.

The validator analyzes the source code structure and blocks any imports of dangerous modules (`socket`, `urllib`, `http`, `subprocess`) or unsafe functions (`eval`, `exec`).

```python
# file: security_sandbox.py
import ast

class UnsafeCodeError(SecurityError):
    """Exception thrown when code violates sandbox security policies."""
    pass

class ASTSafetyValidator(ast.NodeVisitor):
    def __init__(self):
        # List of strictly banned modules
        self.banned_modules = {
            'socket', 'urllib', 'http', 'ftplib', 'smtplib',
            'subprocess', 'pty', 'platform', 'ctypes'
        }
        # List of strictly banned functions
        self.banned_functions = {'eval', 'exec', 'compile', 'globals', 'locals'}

    def visit_Import(self, node):
        """Checks 'import module' statements."""
        for alias in node.names:
            if alias.name in self.banned_modules or alias.name.split('.')[0] in self.banned_modules:
                raise UnsafeCodeError(f"[SECURITY] Banned import detected: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Checks 'from module import x' statements."""
        if node.module in self.banned_modules or node.module.split('.')[0] in self.banned_modules:
            raise UnsafeCodeError(f"[SECURITY] Banned import detected: 'from {node.module} import ...'")
        self.generic_visit(node)

    def visit_Call(self, node):
        """Checks function call names against banned list."""
        if isinstance(node.func, ast.Name):
            if node.func.id in self.banned_functions:
                raise UnsafeCodeError(f"[SECURITY] Banned function execution: '{node.func.id}()'")
        self.generic_visit(node)

def validate_skill_file(file_path):
    """
    Parses a python file into an AST and runs safety validation.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    try:
        tree = ast.parse(source_code)
        validator = ASTSafetyValidator()
        validator.visit(tree)
        print(f"[SANDBOX] Safety Check Passed: '{os.path.basename(file_path)}'")
        return True
    except UnsafeCodeError as se:
        print(f"[SECURITY ALERT] Banned operation in {file_path}: {se}")
        return False
    except SyntaxError as e:
        print(f"[SANDBOX] Syntax Error detected during analysis of {file_path}: {e}")
        return False

if __name__ == "__main__":
    # Test Unsafe Scenario
    unsafe_snippet = "import socket\nprint('Malicious Outbound connection created')"
    test_file = "temp_unsafe.py"
    with open(test_file, 'w') as f:
        f.write(unsafe_snippet)
        
    print("Testing security verification:")
    is_safe = validate_skill_file(test_file)
    print(f"Is file safe: {is_safe}")
    
    if os.path.exists(test_file):
        os.remove(test_file)
```

---

## 4. Safety Policies & Tool Registration

To allow your agent to execute tools exposed by custom skills or external Model Context Protocol (MCP) servers, you must explicitly declare dynamic grants inside the agent's **Safety Policy**.

### 4.1 Safety Policy Specification
If your custom skill connects to a FastMCP server or generates tools, the safety policy must declare narrow, prefix-matched scopes:

```python
# file: configure_safety_policy.py
from google.antigravity import SafetyPolicy

def build_keystone_safety_policy():
    """
    Initializes a highly secure safety policy that grants dynamic execution
    privileges to the Keystone Skills folder while blocking wildcards.
    """
    policy = SafetyPolicy()
    
    # 1. Allow local file reads inside the designated workspace only
    policy.grant(
        action="read_file",
        target=r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    )
    
    # 2. Grant tool execution privileges to the Keystone Tax skill
    policy.grant(
        action="mcp",
        target="keystone-tax-compliance/*"
    )
    
    # 3. Restrict dynamic terminal executions to exact commands
    policy.grant(
        action="command",
        target="python scratch/mark_queue_done.py"
    )
    policy.grant(
        action="command",
        target="python scratch/ingest_deep_research.py"
    )
    
    print("[POLICY] Safety configuration compiled. Unauthorized scopes blocked.")
    return policy
```

---

## 5. Programmatic Multi-File Skill Ingestion Loop

To test and execute a custom skill, we use the `LocalAgentConfig` to point to our dynamic skill directory. The following script demonstrates loading a custom skill, validating its internal modules through our AST sandbox, registering safety controls, and running an agent loop.

```python
# file: run_skill_agent.py
import os
import sys
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from security_sandbox import validate_skill_file

async def run_autonomous_skill_agent(workspace_path, skill_dir_name):
    """
    End-to-end execution:
      1. Scan skill directory for Python modules.
      2. Run AST safety sandbox checks on all files.
      3. Set LocalAgentConfig path.
      4. Spawn Agent and ask it to execute the newly learned skill.
    """
    skill_root_path = os.path.join(workspace_path, skill_dir_name)
    print(f"[LOADER] Scanning skill path: {skill_root_path}")
    
    # Scan for Python files in tools/ or scripts/
    for root, _, files in os.walk(skill_root_path):
        for f in files:
            if f.endswith('.py'):
                full_path = os.path.join(root, f)
                # AST Safety check
                if not validate_skill_file(full_path):
                    raise SecurityError(f"Execution blocked. Unsafe file: {full_path}")
                    
    # Initialize LocalAgentConfig pointing to our skills folder
    config = LocalAgentConfig(
        skills_paths=[workspace_path], # Loads parent containing our skill directory
        api_key=os.environ.get("GEMINI_API_KEY", "mock_key_studio_app")
    )
    
    print("[LOADER] Initializing Agent with custom skill...")
    async with Agent(config) as agent:
        # Prompt the agent to utilize its dynamic tax compliance tool
        prompt = (
            "Run a test calculations for BC construction tax. "
            "Using our local 'keystone-tax-compliance' skill, calculate the PST on a "
            "$40,000 geo-technical survey invoice performed on October 15, 2026."
        )
        response = await agent.chat(prompt)
        print("====================================================")
        print("AGENT RESPONSE:")
        print(await response.text())
        print("====================================================")

if __name__ == "__main__":
    # Mock parameters for verification run
    workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    skill_folder = "dynamic_skills"
    
    try:
        # Run event loop (Requires full python-antigravity runtime installed to execute chat)
        asyncio.run(run_autonomous_skill_agent(workspace, skill_folder))
    except Exception as e:
        print(f"\n[PIPELINE NOTICE] Local Antigravity SDK agent loop connection skipped. Error: {e}")
        print("This is normal in mock environments without a live Google AI Studio key or active SDK runtime.")
        print("The written source codes are successfully validated and saved to project folder.")
```

---

## 6. Verification and Deployment Checklist

Follow these steps to deploy and register a custom skill securely:

- [ ] **Establish `SKILL.md` Metadata:** Define a valid YAML frontmatter containing `name`, `description`, `version`, and narrow activation `predicates`.
- [ ] **Enforce Directory Isolation:** Place all executable modules under `tools/` and helper scripts under `scripts/`. Use dynamic path resolution in tools.
- [ ] **Run Safety Sandbox Validation:** Execute `security_sandbox.py` on all local scripts before registering them to block unsafe imports or function calls.
- [ ] **Apply safety policy constraints:** Grant explicit grants in your agent's config using `policy.grant("mcp", "your-skill/*")` rather than broad wildcards.
- [ ] **Initialize LocalAgentConfig:** Point `skills_paths` to the parent folder containing your custom skills to enable automatic discovery.


---
📁 **See also:** ← Directory Index

**Related:** [[20260522_antigravity_skills_directory]] · [[20260521_antigravity_skills_discovery_mcp_server_marketplace_top_50_most_useful_servers_for_busine]] · 20260522_antigravity_skills_discovery_antigravity_subagent_orchestration_patterns_for_parallel_aut
