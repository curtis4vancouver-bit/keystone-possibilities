import ast
import os
import sys
import subprocess
import pickle
import json
from typing import Dict, Any, List

class SecurityException(Exception):
    """Raised when generated code violates the security policy."""
    pass

class ExecutionLimitError(Exception):
    """Raised when sandboxed execution exceeds memory or CPU bounds."""
    pass

# =========================================================================
# Tier 1: Static AST Parsing and Restricted Execution
# =========================================================================
class SecurityValidator(ast.NodeVisitor):
    def __init__(self):
        # Strict allowed AST node types
        self.allowed_nodes = {
            ast.Module, ast.FunctionDef, ast.arguments, ast.arg,
            ast.Return, ast.Assign, ast.Name, ast.Store, ast.Load,
            ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Constant,
            ast.Call, ast.Attribute, ast.Compare, ast.If, ast.Pass,
            ast.Expr, ast.List, ast.Dict, ast.Tuple, ast.UnaryOp, ast.USub, ast.UAdd, ast.Not,
            ast.Import, ast.ImportFrom, ast.alias,
            ast.BoolOp, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
            ast.Subscript, ast.Slice, ast.IfExp, ast.ListComp, ast.DictComp, ast.comprehension,
            ast.For, ast.While, ast.Break, ast.Continue, ast.Raise, ast.keyword,
            ast.AugAssign, ast.Mod, ast.FloorDiv, ast.JoinedStr, ast.FormattedValue,
            ast.Try, ast.ExceptHandler
        }
        
        # Safe standard library whitelists
        # NOTE: os, sys, pickle removed — security risk (arbitrary code exec, RCE via deserialization)
        self.allowed_modules = {
            "math", "json", "datetime", "re", "urllib", "hashlib",
            "typing", "collections", "time", "functools",
            "dataclasses", "statistics", "string", "textwrap", "csv", "pathlib",
            "os.path", "copy", "enum", "itertools", "operator"
        }
        self.prohibited_attributes = {"__subclasses__", "__getattribute__", "__globals__", "__builtins__", "__code__", "__dict__"}

    def validate_code(self, source_code: str) -> bool:
        """Parses the code to an AST and scans it for prohibited patterns."""
        try:
            parsed_ast = ast.parse(source_code, mode="exec")
            self.visit(parsed_ast)
            return True
        except SecurityException as e:
            raise e
        except Exception as e:
            raise SecurityException(f"Syntax validation failed: {str(e)}")

    def visit(self, node):
        # Enforce structural node boundaries
        if type(node) not in self.allowed_nodes:
            raise SecurityException(f"Prohibited code construct identified: {type(node).__name__}")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name not in self.allowed_modules:
                raise SecurityException(f"Import of module '{alias.name}' is prohibited.")
        self.generic_visit(node)
                
    def visit_ImportFrom(self, node):
        if node.module not in self.allowed_modules:
            raise SecurityException(f"Import from module '{node.module}' is prohibited.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Check attribute names to block dunder sandboxing escapes
        if node.attr in self.prohibited_attributes:
            raise SecurityException(f"Prohibited attribute access detected: '{node.attr}'")
        
        # Prevent TOCTOU mutations via double under prefixes
        if isinstance(node.value, ast.Name) and node.value.id.startswith("__"):
            raise SecurityException("Dynamic naming manipulation is prohibited.")
        self.generic_visit(node)

# =========================================================================
# Tier 2: Isolated Process Execution (PEP 734 Emulator)
# =========================================================================
def run_isolated_skill(module_name: str, function_name: str, input_args: Dict[str, Any], timeout_sec: float = 10.0) -> Any:
    """
    Executes a dynamic module function in a completely isolated process namespace.
    Mimics PEP 734 execution queues using localized pickle IPC.
    Ensures complete memory, global state, and GIL separation.
    """
    temp_dir = os.path.join(os.getcwd(), "scratch", "sandbox_runs")
    os.makedirs(temp_dir, exist_ok=True)
    
    args_file = os.path.join(temp_dir, f"{module_name}_args.pkl")
    res_file = os.path.join(temp_dir, f"{module_name}_res.pkl")
    
    # Serialize argument data
    with open(args_file, "wb") as f:
        pickle.dump(input_args, f)
        
    # Python code wrapper to run the target module and capture output
    runner_script = f"""
import sys
import os
import pickle
import traceback

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "dynamic_skills"))

try:
    import importlib
    skill_module = importlib.import_module("{module_name}")
    target_func = getattr(skill_module, "{function_name}")
    
    with open(r"{args_file}", "rb") as f:
        args = pickle.load(f)
        
    # Execute in isolated space
    result = target_func(**args)
    
    with open(r"{res_file}", "wb") as f:
        pickle.dump({{"status": "success", "data": result}}, f)
except Exception as e:
    tb = traceback.format_exc()
    with open(r"{res_file}", "wb") as f:
        pickle.dump({{"status": "error", "message": str(e), "traceback": tb}}, f)
"""
    
    script_file = os.path.join(temp_dir, f"{module_name}_runner.py")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(runner_script)
        
    try:
        # Run subprocess under strict timeout
        res = subprocess.run(
            [sys.executable, script_file],
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        
        if not os.path.exists(res_file):
            raise ExecutionLimitError(f"Subprocess terminated unexpectedly: {res.stderr}")
            
        with open(res_file, "rb") as f:
            output = pickle.load(f)
            
        if output["status"] == "success":
            return output["data"]
        else:
            raise RuntimeError(f"Skill error: {output['message']}\nTraceback:\n{output['traceback']}")
            
    except subprocess.TimeoutExpired:
        raise ExecutionLimitError(f"Execution exceeded strict latency budget of {timeout_sec}s.")
    finally:
        # Clean up files
        for path in [args_file, res_file, script_file]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

# =========================================================================
# Tier 3: Hypervisor Isolation (.wsb XML Compiler)
# =========================================================================
def compile_windows_sandbox_config(sandbox_name: str, src_folder: str, out_folder: str) -> str:
    """
    Dynamically generates a .wsb configuration file to run high-risk test scripts 
    inside a disposable Hyper-V sandbox wrapper on Windows 11.
    """
    os.makedirs(out_folder, exist_ok=True)
    wsb_xml = f"""<Configuration>
  <Networking>Disable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>{os.path.abspath(src_folder)}</HostFolder>
      <SandboxFolder>C:\\SandboxWorkspace</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>{os.path.abspath(out_folder)}</HostFolder>
      <SandboxFolder>C:\\SandboxOutput</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>cmd.exe /c "python C:\\SandboxWorkspace\\automated_runner.py --src C:\\SandboxWorkspace --out C:\\SandboxOutput"</Command>
  </LogonCommand>
</Configuration>
"""
    wsb_path = os.path.abspath(f"{sandbox_name}.wsb")
    with open(wsb_path, "w", encoding="utf-8") as f:
        f.write(wsb_xml)
    return wsb_path

def pre_command_hook(command: str) -> bool:
    """
    Validates shell (bash/PowerShell) commands before execution.
    Returns True if safe, raises SecurityException if blocked.
    """
    blocked_keywords = [
        "rm -rf /", "Format-Volume", "Remove-Item *", 
        "del /s", "drop database", "shutdown", "reboot"
    ]
    for keyword in blocked_keywords:
        if keyword.lower() in command.lower():
            raise SecurityException(f"Command execution blocked: Contains prohibited action '{keyword}'")
    return True

# =========================================================================
# Tier 4: PreToolUse Security Hooks (Agent Tool-Call Interception Layer)
# =========================================================================
# Research Source: 20260610_AGENT_ARCH_pretooluse_hook_security_patterns
# Implements: Synchronous tool-call interception, destructive command blocking,
#             audit trail logging, and --dry-run argument injection for testing.
# Pattern: Treat the LLM as an unreliable subcontractor. The hooks execute the contract.

import datetime as _dt
import re as _re
import logging as _logging

# ─── Audit Logger Setup ──────────────────────────────────────────────────
_AUDIT_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".learnings")
os.makedirs(_AUDIT_LOG_DIR, exist_ok=True)
_AUDIT_LOG_PATH = os.path.join(_AUDIT_LOG_DIR, "tool_audit.log")

_audit_logger = _logging.getLogger("keystone_tool_audit")
_audit_logger.setLevel(_logging.INFO)
if not _audit_logger.handlers:
    _audit_handler = _logging.FileHandler(_AUDIT_LOG_PATH, encoding="utf-8")
    _audit_handler.setFormatter(_logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    _audit_logger.addHandler(_audit_handler)

# ─── Dangerous Pattern Blocklist ─────────────────────────────────────────
# Each entry is (pattern_regex, description, severity)
DANGEROUS_PATTERNS: List[Dict[str, str]] = [
    # Shell — destructive file operations
    {"pattern": r"rm\s+-rf\s+/", "description": "Recursive root deletion", "severity": "CRITICAL"},
    {"pattern": r"rm\s+-rf\s+~", "description": "Recursive home directory deletion", "severity": "CRITICAL"},
    {"pattern": r"rm\s+-rf\s+\*", "description": "Recursive wildcard deletion", "severity": "CRITICAL"},
    {"pattern": r"rm\s+-rf\s+\.", "description": "Recursive current directory deletion", "severity": "CRITICAL"},
    {"pattern": r"del\s+/[fFsSqQ]", "description": "Windows forced delete", "severity": "HIGH"},
    {"pattern": r"del\s+/s\s+/q", "description": "Windows silent recursive delete", "severity": "CRITICAL"},
    {"pattern": r"rmdir\s+/[sS]\s+/[qQ]", "description": "Windows recursive directory removal", "severity": "CRITICAL"},
    {"pattern": r"format\s+[a-zA-Z]:", "description": "Disk format command", "severity": "CRITICAL"},
    {"pattern": r"Format-Volume", "description": "PowerShell volume format", "severity": "CRITICAL"},
    {"pattern": r"Remove-Item\s+.*-Recurse.*-Force", "description": "PowerShell recursive force delete", "severity": "CRITICAL"},
    {"pattern": r"Clear-Content\s+.*\*", "description": "PowerShell wildcard content clear", "severity": "HIGH"},
    
    # Shell — system disruption
    {"pattern": r"shutdown\s+/[sSpP]", "description": "System shutdown command", "severity": "HIGH"},
    {"pattern": r"Stop-Computer", "description": "PowerShell shutdown", "severity": "HIGH"},
    {"pattern": r"Restart-Computer", "description": "PowerShell restart", "severity": "HIGH"},
    {"pattern": r">\s*/dev/sd[a-z]", "description": "Direct disk write (Linux)", "severity": "CRITICAL"},
    {"pattern": r"mkfs\.", "description": "Filesystem creation on device", "severity": "CRITICAL"},
    {"pattern": r"dd\s+if=.*of=/dev/", "description": "Raw disk write via dd", "severity": "CRITICAL"},
    
    # SQL — destructive operations
    {"pattern": r"DROP\s+TABLE", "description": "SQL table drop", "severity": "CRITICAL"},
    {"pattern": r"DROP\s+DATABASE", "description": "SQL database drop", "severity": "CRITICAL"},
    {"pattern": r"TRUNCATE\s+TABLE", "description": "SQL table truncation", "severity": "HIGH"},
    {"pattern": r"DELETE\s+FROM\s+\w+\s*;?\s*$", "description": "SQL delete without WHERE clause", "severity": "HIGH"},
    {"pattern": r"ALTER\s+TABLE\s+\w+\s+DROP", "description": "SQL column drop", "severity": "HIGH"},
    
    # Network — exfiltration patterns
    {"pattern": r"curl\s+.*-d\s+.*password", "description": "Credential exfiltration via curl", "severity": "CRITICAL"},
    {"pattern": r"wget\s+.*\|\s*sh", "description": "Remote code execution via wget pipe", "severity": "CRITICAL"},
    {"pattern": r"Invoke-WebRequest.*\|\s*iex", "description": "PowerShell remote code exec", "severity": "CRITICAL"},
    
    # Registry — Windows system modification
    {"pattern": r"reg\s+delete\s+HKLM", "description": "Windows registry delete (HKLM)", "severity": "CRITICAL"},
    {"pattern": r"Remove-ItemProperty.*HKLM", "description": "PowerShell registry property removal", "severity": "CRITICAL"},
]

# Compiled regex cache for performance
_COMPILED_PATTERNS = [(
    _re.compile(p["pattern"], _re.IGNORECASE),
    p["description"],
    p["severity"]
) for p in DANGEROUS_PATTERNS]

# ─── Dry-Run Injection Targets ───────────────────────────────────────────
# Tools that should have --dry-run injected when DRY_RUN_MODE is active
DRY_RUN_INJECTABLE_TOOLS = {
    "deploy", "publish", "upload", "push", "migrate", "sync",
    "social_publish", "push_to_production", "deploy_content",
}

# Global dry-run mode flag (set via env var or programmatically)
DRY_RUN_MODE = os.environ.get("KEYSTONE_DRY_RUN", "").lower() in ("1", "true", "yes")


class PreToolCheckResult:
    """Result of a pre-tool security check."""
    
    def __init__(self, allowed: bool, tool_name: str, reason: str = "",
                 severity: str = "INFO", mutated_args: Dict[str, Any] = None):
        self.allowed = allowed
        self.tool_name = tool_name
        self.reason = reason
        self.severity = severity
        self.mutated_args = mutated_args  # Non-None if args were modified (e.g., dry-run injected)
    
    def __bool__(self):
        return self.allowed
    
    def __repr__(self):
        status = "ALLOWED" if self.allowed else "BLOCKED"
        return f"PreToolCheckResult({status}, tool={self.tool_name}, reason={self.reason})"


def pre_tool_check(tool_name: str, args: Dict[str, Any],
                   dry_run_override: bool = None) -> PreToolCheckResult:
    """
    PreToolUse synchronous interception gate.
    
    Validates tool arguments against the dangerous pattern blocklist before
    execution. Blocks destructive commands, logs all tool calls for audit
    trails, and optionally injects --dry-run flags.
    
    Args:
        tool_name: Name of the tool being invoked
        args: Dictionary of arguments being passed to the tool
        dry_run_override: If True/False, overrides the global DRY_RUN_MODE setting
    
    Returns:
        PreToolCheckResult with allowed=True/False and optional mutated_args
    
    Usage:
        result = pre_tool_check("Bash", {"command": "rm -rf /"})
        if not result:
            print(f"BLOCKED: {result.reason}")
        else:
            # Safe to execute, use result.mutated_args if not None
            execute_tool(tool_name, result.mutated_args or args)
    """
    timestamp = _dt.datetime.now().isoformat()
    args_str = json.dumps(args, default=str) if isinstance(args, dict) else str(args)
    
    # 1. Audit Trail — Log EVERY tool call regardless of outcome
    _audit_logger.info(f"TOOL_CALL | tool={tool_name} | args={args_str[:500]}")
    
    # 2. Scan arguments against dangerous patterns
    # Flatten all argument values into a single scannable string
    scan_text = _flatten_args_for_scan(args)
    
    for compiled_re, description, severity in _COMPILED_PATTERNS:
        if compiled_re.search(scan_text):
            # BLOCKED — log the violation
            block_msg = (
                f"Destructive pattern detected: {description} | "
                f"Severity: {severity} | Tool: {tool_name} | "
                f"Args snippet: {args_str[:200]}"
            )
            _audit_logger.warning(f"BLOCKED | {block_msg}")
            print(f"[PreToolUse] BLOCKED: {description} (severity: {severity})")
            
            return PreToolCheckResult(
                allowed=False,
                tool_name=tool_name,
                reason=f"Destructive pattern: {description}",
                severity=severity,
            )
    
    # 3. Dry-Run Injection — mutate args if applicable
    use_dry_run = dry_run_override if dry_run_override is not None else DRY_RUN_MODE
    mutated_args = None
    
    if use_dry_run and tool_name.lower() in DRY_RUN_INJECTABLE_TOOLS:
        mutated_args = dict(args)  # Shallow copy
        if "flags" not in mutated_args:
            mutated_args["flags"] = []
        if isinstance(mutated_args["flags"], list) and "--dry-run" not in mutated_args["flags"]:
            mutated_args["flags"].append("--dry-run")
            _audit_logger.info(f"DRY_RUN_INJECTED | tool={tool_name} | --dry-run flag added")
            print(f"[PreToolUse] DRY-RUN injected for {tool_name}")
    
    # 4. ALLOWED
    _audit_logger.info(f"ALLOWED | tool={tool_name}")
    
    return PreToolCheckResult(
        allowed=True,
        tool_name=tool_name,
        reason="Passed all security checks",
        severity="INFO",
        mutated_args=mutated_args,
    )


def _flatten_args_for_scan(args: Any) -> str:
    """Recursively flattens argument values into a single string for pattern scanning."""
    if isinstance(args, str):
        return args
    if isinstance(args, dict):
        parts = []
        for v in args.values():
            parts.append(_flatten_args_for_scan(v))
        return " ".join(parts)
    if isinstance(args, (list, tuple)):
        return " ".join(_flatten_args_for_scan(item) for item in args)
    return str(args) if args is not None else ""


def get_audit_log_path() -> str:
    """Returns the path to the tool audit log file."""
    return _AUDIT_LOG_PATH


def get_audit_tail(n_lines: int = 20) -> List[str]:
    """Returns the last n lines from the audit log."""
    if not os.path.exists(_AUDIT_LOG_PATH):
        return []
    try:
        with open(_AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-n_lines:]]
    except Exception:
        return []


def post_execution_hook(modified_files: List[str] = None):
    """
    Post-execution hook to auto-ingest modified files into Qdrant collections.
    """
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(url="http://localhost:6333")
        client.set_model("BAAI/bge-small-en-v1.5")
    except Exception:
        print("[Post-Hook] Qdrant offline, skipping auto-ingestion.")
        return

    if modified_files is None:
        import time
        modified_files = []
        project_root = os.getcwd()
        current_time = time.time()
        for root, dirs, files in os.walk(project_root):
            if any(p in root for p in ["venv", ".git", ".learnings", "scratch", ".agents", "MCP_Multiplexer"]):
                continue
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(path)
                        if current_time - mtime < 120:  # modified within last 2 minutes
                            modified_files.append(path)
                    except Exception:
                        pass

    if not modified_files:
        return

    print(f"[Post-Hook] Auto-ingesting {len(modified_files)} modified file(s)...")
    for filepath in modified_files:
        filename = os.path.basename(filepath)
        namespace = "general"
        filepath_lower = filepath.lower()
        if "possibilities" in filepath_lower:
            namespace = "possibilities"
        elif "music" in filepath_lower:
            namespace = "music"
        elif "protocol" in filepath_lower or "health" in filepath_lower:
            namespace = "protocol"
        elif "master" in filepath_lower:
            namespace = "master"
        elif "webmaster" in filepath_lower:
            namespace = "webmaster"
        elif "research" in filepath_lower:
            namespace = "research_scout"
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            if not client.collection_exists(collection_name=namespace):
                client.create_collection(
                    collection_name=namespace,
                    vectors_config=client.get_fastembed_vector_params()
                )
                
            # Chunk and add
            chunks = []
            chunk_size = 1000
            overlap = 200
            start = 0
            while start < len(content):
                end = start + chunk_size
                chunks.append(content[start:end])
                start += chunk_size - overlap
                
            docs = chunks
            meta = [{"source": filename, "filepath": filepath, "chunk_index": i} for i in range(len(chunks))]
            client.add(collection_name=namespace, documents=docs, metadata=meta)
            print(f"  [Post-Hook] Auto-ingested {filename} into namespace '{namespace}' ({len(chunks)} chunks).")
        except Exception as e:
            print(f"  [Post-Hook] Failed to ingest {filename}: {e}")
