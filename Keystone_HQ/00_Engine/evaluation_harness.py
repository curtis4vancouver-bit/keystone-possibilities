import os
import time
import sqlite3
import json
import re
from typing import Dict, Any, List
from pydantic import BaseModel
from security_sandbox import run_isolated_skill, SecurityValidator, SecurityException

def generate_and_run_pytest(module_name: str, function_name: str, fixtures: List[Dict[str, Any]]) -> bool:
    """
    Translates JSON fixtures into a standard pytest file and runs it via subprocess.
    """
    test_code = [
        "import pytest",
        "import sys",
        "import os",
        "",
        "# Add dynamic_skills path to sys.path",
        "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
        f"from dynamic_skills import {module_name}",
        ""
    ]
    
    for idx, case in enumerate(fixtures):
        input_args = case.get("input", {})
        assertions = case.get("assertions", [])
        
        test_code.append(f"def test_{function_name}_case_{idx}():")
        test_code.append(f"    input_args = {repr(input_args)}")
        test_code.append(f"    res = {module_name}.{function_name}(**input_args)")
        
        for assertion in assertions:
            a_type = assertion.get("type")
            target = assertion.get("target")
            
            if a_type == "regex":
                pattern = assertion.get("pattern", "")
                if target:
                    test_code.append(f"    import re")
                    test_code.append(f"    assert re.search({repr(pattern)}, str(res.get({repr(target)})))")
                else:
                    test_code.append(f"    import re")
                    test_code.append(f"    assert re.search({repr(pattern)}, str(res))")
            elif a_type == "exact":
                expected = assertion.get("value")
                if target:
                    test_code.append(f"    assert res.get({repr(target)}) == {repr(expected)}")
                else:
                    test_code.append(f"    assert res == {repr(expected)}")
            elif a_type == "schema":
                required_keys = assertion.get("keys", [])
                test_code.append(f"    assert isinstance(res, dict)")
                for k in required_keys:
                    test_code.append(f"    assert {repr(k)} in res")
        test_code.append("")
        
    test_filepath = os.path.join("scratch", f"test_{module_name}.py")
    os.makedirs(os.path.dirname(test_filepath), exist_ok=True)
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(test_code))
        
    print(f"[Pytest Generator] Pytest file generated: {test_filepath}")
    
    # Execute pytest in subprocess
    try:
        import subprocess
        res = subprocess.run(
            ["pytest", test_filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if res.returncode == 0:
            print("[Pytest Runner] pytest check PASSED ✅")
            return True
        else:
            print(f"[Pytest Runner] pytest check FAILED ❌\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
            return False
    except Exception as e:
        print(f"[Pytest Runner] pytest run crash: {e}")
        return False

DB_PATH = os.path.join("scratch", "rolling_results.db")

class EvaluationResult(BaseModel):
    is_valid: bool
    accuracy_score: float
    token_cost: float
    execution_time_ms: float
    performance_score: float
    message: str

def init_results_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            module_name TEXT,
            function_name TEXT,
            accuracy_score REAL,
            token_cost REAL,
            execution_time_ms REAL,
            performance_score REAL,
            status TEXT,
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()

def execute_fixture_tests(module_name: str, function_name: str, fixtures_path: str, alpha: float = 1.0, beta: float = 0.05, gamma: float = 0.001) -> EvaluationResult:
    """
    Executes a synthesized module against deterministic test fixtures.
    Validates safety policies, processes assertions, and logs metrics.
    """
    init_results_db()
    
    # 1. Safety AST Validation Check
    source_file = os.path.join("dynamic_skills", f"{module_name}.py")
    if not os.path.exists(source_file):
        # Fallback to local search
        source_file = os.path.join(os.getcwd(), f"{module_name}.py")
        if not os.path.exists(source_file):
            return EvaluationResult(
                is_valid=False,
                accuracy_score=0.0,
                token_cost=0.0,
                execution_time_ms=0.0,
                performance_score=0.0,
                message=f"Error: Source file '{module_name}.py' not found."
            )
            
    with open(source_file, "r", encoding="utf-8") as f:
        source_code = f.read()
        
    validator = SecurityValidator()
    try:
        validator.validate_code(source_code)
    except SecurityException as e:
        return EvaluationResult(
            is_valid=False,
            accuracy_score=0.0,
            token_cost=0.0,
            execution_time_ms=0.0,
            performance_score=-1.0,
            message=f"Safety Exception: AST check failed: {str(e)}"
        )
        
    # 2. Ingest Test Fixtures
    if not os.path.exists(fixtures_path):
        return EvaluationResult(
            is_valid=False,
            accuracy_score=0.0,
            token_cost=0.0,
            execution_time_ms=0.0,
            performance_score=0.0,
            message=f"Error: Fixtures file '{fixtures_path}' not found."
        )
        
    with open(fixtures_path, "r", encoding="utf-8") as f:
        fixtures = json.load(f)

    # 2b. Automated pytest Generation & Subprocess Run
    pytest_ok = generate_and_run_pytest(module_name, function_name, fixtures)
    if not pytest_ok:
        return EvaluationResult(
            is_valid=False,
            accuracy_score=0.0,
            token_cost=0.0,
            execution_time_ms=0.0,
            performance_score=-0.5,
            message="Pytest validation stage failed."
        )
        
    total_tests = len(fixtures)
    passed_tests = 0
    total_latency_ms = 0.0
    
    # Mocking standard token pricing for calculations
    # Input pricing: $0.00125 per 1K chars, output: $0.005 per 1K chars
    approx_token_cost = (len(source_code) / 1000.0) * 0.00125
    
    print(f"\n[Test Runner] Executing {total_tests} test cases for {module_name}.{function_name}...")
    
    for idx, case in enumerate(fixtures):
        input_args = case.get("input", {})
        assertions = case.get("assertions", [])
        
        start_time = time.perf_counter()
        try:
            # Execute within isolated process sandbox
            res = run_isolated_skill(module_name, function_name, input_args)
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            total_latency_ms += latency_ms
            
            # Execute assertions
            case_passed = True
            for assertion in assertions:
                a_type = assertion.get("type")
                target = assertion.get("target")
                
                # Check for assertions
                if a_type == "regex":
                    pattern = assertion.get("pattern", "")
                    val_to_check = res.get(target) if (target and isinstance(res, dict)) else res
                    if not re.search(pattern, str(val_to_check)):
                        print(f"  [FAIL] Test {idx+1}: Pattern '{pattern}' not matched in target '{target}' (value: '{val_to_check}')")
                        case_passed = False
                        break
                elif a_type == "exact":
                    expected = assertion.get("value")
                    val_to_check = res.get(target) if (target and isinstance(res, dict)) else res
                    if val_to_check != expected:
                        print(f"  [FAIL] Test {idx+1}: Target '{target}' - Expected '{expected}', got '{val_to_check}'")
                        case_passed = False
                        break
                elif a_type == "schema":
                    required_keys = assertion.get("keys", [])
                    if not isinstance(res, dict) or not all(k in res for k in required_keys):
                        print(f"  [FAIL] Test {idx+1}: Response dictionary missing required keys: {required_keys}")
                        case_passed = False
                        break
            
            if case_passed:
                passed_tests += 1
                
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            total_latency_ms += latency_ms
            print(f"  [FAIL] Test {idx+1} execution crashed: {str(e)}")
            
    accuracy = passed_tests / total_tests if total_tests > 0 else 0.0
    avg_latency = total_latency_ms / total_tests if total_tests > 0 else 0.0
    
    # Calculate performance score: S(p) = alpha * A(p) - beta * C(p) - gamma * T(p)
    performance = (alpha * accuracy) - (beta * approx_token_cost) - (gamma * avg_latency)
    
    # 3. Log to rolling SQLite DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO runs (module_name, function_name, accuracy_score, token_cost, execution_time_ms, performance_score, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        module_name,
        function_name,
        accuracy,
        approx_token_cost,
        avg_latency,
        performance,
        "PASS" if accuracy == 1.0 else "FAIL",
        None if accuracy == 1.0 else f"Failed {total_tests - passed_tests} out of {total_tests} test cases."
    ))
    conn.commit()
    conn.close()
    
    message = f"Execution completed. Accuracy: {passed_tests}/{total_tests} ({accuracy*100:.1f}%), Avg Latency: {avg_latency:.1f}ms, Performance Score: {performance:.4f}"
    print(f"[Test Runner] {message}")
    
    return EvaluationResult(
        is_valid=(accuracy == 1.0),
        accuracy_score=accuracy,
        token_cost=approx_token_cost,
        execution_time_ms=avg_latency,
        performance_score=performance,
        message=message
    )
