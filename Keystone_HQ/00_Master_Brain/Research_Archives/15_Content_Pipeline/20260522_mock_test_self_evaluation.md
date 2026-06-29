# Mock Test Generation for AI Agent Self-Evaluation

**Research Date:** May 22, 2026
**Domain:** self_learning_patterns
**Author:** Keystone Overnight Research Agent

---

## Executive Summary

Testing AI [[AGENTS|agents]] demands fundamentally different strategies than testing traditional software. [[AGENTS|Agents]] are non-deterministic, multi-step, and autonomous -- meaning a simple `assert output == expected` approach is brittle and insufficient. This report covers the full landscape of mock test generation and self-evaluation for AI [[AGENTS|agents]], from property-based testing of tool routing, to snapshot-based regression detection, to CI/CD pipelines for continuous quality monitoring. The goal is to provide Keystone with actionable patterns for building a self-testing framework that validates agent behavior without incurring real API costs, tracks improvement over time, and catches regressions before they reach production.

---

## 1. Self-Testing Frameworks for AI [[AGENTS|Agents]]

### The 2025-2026 Landscape

The testing ecosystem has matured significantly. Key frameworks include:

| Framework | Best For | Key Feature |
|:---|:---|:---|
| **DeepEval** | CI/CD-native pytest testing | 50+ built-in metrics, `ToolCorrectnessMetric` |
| **Promptfoo** | Declarative YAML-based evals | Multi-model comparison, `llm-rubric` assertions |
| **Maxim AI** | Multi-turn agent simulation | Replay production traces, component-level eval |
| **LangSmith** | LangChain ecosystem tracing | Deep debugging, multi-turn evaluation templates |
| **Arize Phoenix** | Observability-first evaluation | Trace complex reasoning, tool-call analysis |
| **Opik (Comet)** | Agent reliability | LLM-as-a-judge, CI/CD integration |
| **Ragas** | RAG pipeline evaluation | Context precision, recall, faithfulness |
| **Braintrust** | CI/CD eval gates | Logging, scoring, regression detection |

### Architecture for Self-Testing

A robust self-testing framework evaluates [[AGENTS|agents]] at four levels:

1. **Component Level** -- Individual tools, parsers, memory logic tested in isolation.
2. **Routing Level** -- Does the agent select the correct tool for a given intent?
3. **Trajectory Level** -- Is the sequence of actions (thought -> tool call -> result -> next action) sound?
4. **Outcome Level** -- Does the agent actually solve the user's problem?

---

## 2. Mock Test Patterns for Agent Behavior

### Strategy: Mock Tools, Not the LLM

The key insight is to mock at the tool/function layer rather than replacing the entire LLM. This verifies that orchestration logic, tool selection, and parameter formatting work correctly without executing real side effects.

### Core Patterns

**Pattern 1: Tool-Level Mocking with unittest.mock**

```python
import pytest
from unittest.mock import MagicMock
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ToolCorrectnessMetric

def test_agent_selects_correct_tool():
    # Mock all available tools
    mock_search = MagicMock(return_value={"results": ["item1"]})
    mock_delete = MagicMock()
    tools = {"search_database": mock_search, "delete_record": mock_delete}
    
    # Run agent with mocked tools
    result = my_agent("Find records for project Alpha", tools)
    
    # Verify correct tool was called, dangerous one was NOT
    mock_search.assert_called_once()
    mock_delete.assert_not_called()
    
    # Evaluate with DeepEval metric
    metric = ToolCorrectnessMetric(threshold=0.7)
    test_case = LLMTestCase(
        input="Find records for project Alpha",
        actual_output=result,
        expected_tools=["search_database"]
    )
    assert_test(test_case, [metric])
```

**Pattern 2: Dry-Run / Simulation Mode**

Design [[AGENTS|agents]] to support a `dry_run=True` parameter where they plan actions but do not execute them. This tests multi-step reasoning chains without any side effects.

**Pattern 3: Service Virtualization for API Faults**

Use mock servers (or simple fixtures) to simulate API timeouts, malformed responses, and rate limits:

```python
def test_agent_handles_api_timeout():
    mock_api = MagicMock(side_effect=TimeoutError("Connection timed out"))
    tools = {"external_api": mock_api}
    
    result = my_agent("Fetch latest data from API", tools)
    
    # Agent should gracefully degrade, not crash
    assert "unable to reach" in result.lower() or "fallback" in result.lower()
    assert not result.startswith("Error:")  # Should be user-friendly
```

**Pattern 4: LLM Provider Mocking**

For testing orchestration plumbing (memory, [[STATE|state]] management, routing logic), intercept LLM calls and return pre-defined deterministic responses. This removes cost and latency from tests entirely.

---

## 3. Property-Based Testing for Tool Routing

Property-based testing (PBT) with Python's `hypothesis` library shifts the focus from checking specific outputs to verifying invariants -- rules that must always hold true regardless of input.

### Key Invariants for Agent Testing

| Invariant | Example Rule |
|:---|:---|
| **Safety** | "For ANY query, the agent must NEVER call `delete_database`." |
| **Ordering** | "For financial queries, `compliance_check` must be called BEFORE any execution tool." |
| **Parameter Integrity** | "Any `send_email` call must contain a valid email format in `to`." |
| **Tool Necessity** | "Simple factual questions must NOT trigger external API calls." |
| **Positional Invariance** | "Shuffling tool order in the prompt must not change the selected tool." |

### Implementation with Hypothesis

```python
from hypothesis import given, strategies as st, settings

# Strategy: generate varied user queries about weather
weather_queries = st.sampled_from([
    "What's the weather in Tokyo?",
    "Is it raining in Seattle right now?",
    "Temperature forecast for London tomorrow",
    "Will it snow in Denver this weekend?",
])

@given(query=weather_queries)
@settings(max_examples=50)
def test_weather_queries_always_route_to_weather_tool(query):
    trace = run_agent_with_tracing(query, dry_run=True)
    
    # Invariant: weather queries must route to weather tool
    tools_called = [step.tool_name for step in trace.steps]
    assert "get_weather" in tools_called, f"Failed for: {query}"
    
    # Safety invariant: must never call destructive tools
    forbidden = {"delete_file", "drop_table", "send_payment"}
    assert not forbidden.intersection(tools_called)
```

### Stateful Testing with RuleBasedStateMachine

For [[AGENTS|agents]] with memory or multi-turn conversations, Hypothesis's `RuleBasedStateMachine` can generate random sequences of user actions (queries, context updates, memory clears) to uncover [[STATE|state]]-related bugs.

---

## 4. Snapshot Testing for Agent Responses

Snapshot testing pins the agent's execution trajectory (not the text output) and diffs against a baseline to detect regressions.

### What to Snapshot

- Sequence of tool calls and their arguments
- Decision branch points (e.g., "decided to search vs. answer directly")
- Key structured outputs (JSON schemas, extracted entities)
- Do NOT snapshot exact prose -- minor wording changes create false positives

### Workflow

1. **Record:** Run agent at `temperature=0`, save trace as JSON snapshot.
2. **Change:** Update prompts, model version, or tool configs.
3. **Replay:** Run same inputs, generate new trace.
4. **Diff:** Compare new trace against snapshot. Flag deviations in tool order, missing calls, or changed parameters.

### Best Practices

- **Redact volatile fields** (timestamps, session IDs) before comparison.
- **Build a Golden Dataset** of 50-100 curated real-world examples covering critical paths, edge cases, and multi-turn workflows.
- **Combine with behavioral assertions:** e.g., "The agent must call `search_calendar` at least once."

---

## 5. Auto-Generating Tests from Execution Traces

Production traces are a goldmine for test case generation. The pipeline works as follows:

1. **Capture:** Use observability tools (LangSmith, Langfuse, Arize) to log every agent execution trace in production.
2. **Cluster:** Group similar execution paths. Identify recurring flows and anomalies.
3. **Synthesize:** Use an LLM to convert interesting traces into structured test cases with inputs, expected tool sequences, and success criteria.
4. **Validate:** Human review before adding to the regression suite.

### Keystone Implementation Sketch

```python
def generate_tests_from_traces(traces: list[AgentTrace]) -> list[TestCase]:
    """Convert production traces into regression test cases."""
    test_cases = []
    for trace in traces:
        if trace.was_successful and trace.is_representative:
            test_cases.append(TestCase(
                input=trace.user_query,
                expected_tool_sequence=[s.tool for s in trace.steps],
                expected_outcome_contains=trace.key_entities,
                source_trace_id=trace.id,
            ))
    return test_cases
```

**Privacy Note:** Mask PII and sensitive data before using production logs for test generation.

---

## 6. Testing Error Recovery and Fallback Behavior

### Fault Injection Categories

| Fault Type | What to Test |
|:---|:---|
| **Tool/API Faults** | Timeouts, 500 errors, malformed JSON responses |
| **Reasoning Faults** | Contradictory instructions, ambiguous queries |
| **Memory Faults** | Context overflow, missing conversation history |
| **Adversarial Inputs** | Prompt injection, privilege escalation attempts |

### Design Patterns for Resilience

- **Circuit Breakers:** Stop agent loops exceeding token budgets or repetition thresholds.
- **Graceful Degradation:** If primary model/tool fails, route to simpler fallback.
- **Retry with Backoff:** Intelligent retries with max attempt limits.
- **Human Escalation:** Hand over to human when confidence drops below threshold.

### Key Metrics

- **Mean Time to Recovery (MTTR):** How quickly the agent returns to a stable [[STATE|state]].
- **Task Completion Rate Under Stress:** Percentage of workflows completed despite injected faults.
- **Confidence Calibration:** How accurately the agent estimates its own uncertainty.

---

## 7. Measuring Agent Improvement Over Time

### Metric Categories

| Category | Metrics | Improvement Signal |
|:---|:---|:---|
| **Outcome** | Task Completion Rate, Resolution Rate | Higher completion without human help |
| **Efficiency** | Cost per Successful Task, Cycle Time | Lower cost, faster resolution |
| **Reliability** | Escalation Rate, Error Recovery Rate | Fewer escalations over time |
| **Quality** | Tool Selection Accuracy, Hallucination Rate | More accurate tool picks, fewer hallucinations |
| **Trust** | Autonomy Level, User Adoption Rate | Users grant more auto-approval |

### Tracking Strategy

- **Development:** Automated benchmark suites on every commit.
- **Production:** Continuous observability with Langfuse/Phoenix/Braintrust.
- **Feedback Loop:** Human-in-the-loop reviews feed back into evaluation metrics.

**Critical Rule:** If you cannot trace a KPI movement back to a specific change (new prompt, different model, updated tool), your measurement layer is not granular enough.

---

## 8. Benchmarking Agent Response Quality

### The Composite Evaluation Approach

No single metric captures agent quality. Use a layered strategy:

1. **Deterministic Code Checks** -- Required fields present, forbidden tools not called, JSON schema valid.
2. **LLM-as-a-Judge** -- Use a strong model to score reasoning quality, faithfulness, and relevance using predefined rubrics. Aim for >0.80 Spearman correlation with human expert judgment.
3. **Human Expert Review** -- Final authority for high-stakes decisions and edge cases.

### Promptfoo YAML for Regression Testing

```yaml
# promptfooconfig.yaml
prompts: [prompts/agent_system_prompt.txt]
providers: [openai:gpt-4o]
tests:
  - vars:
      query: "Search for recent invoices from Acme Corp"
    assert:
      - type: llm-rubric
        value: "Must mention searching a database or document store"
      - type: contains
        value: "Acme"
      - type: not-contains
        value: "I don't know"
  - vars:
      query: "Delete all project files"
    assert:
      - type: llm-rubric
        value: "Must refuse or ask for confirmation before destructive action"
```

---

## 9. CI/CD Pipelines for Continuous Agent Quality

### Pipeline Architecture

```
Code/Prompt Change
    |
    v
[CI Trigger] --> [Lint + Unit Tests]
    |
    v
[Agent Eval Suite] --> DeepEval / Promptfoo
    |                   - Tool routing tests
    |                   - Snapshot regression tests
    |                   - Property-based invariant tests
    v
[Quality Gate] --> Pass threshold? (e.g., >95% tool accuracy)
    |
    v
[Deploy to Staging] --> [Production Monitoring]
                         - Drift detection
                         - Live trace analysis
                         - Automated alerting
```

### Implementation with GitHub Actions

```yaml
# .github/workflows/agent-eval.yml
name: Agent Evaluation
on:
  push:
    paths: ['prompts/**', 'agent/**', 'tools/**']

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install deepeval promptfoo hypothesis
      
      - name: Run property-based tests
        run: pytest tests/test_agent_properties.py -v
      
      - name: Run snapshot regression tests
        run: pytest tests/test_agent_snapshots.py -v
      
      - name: Run DeepEval metrics
        run: deepeval test run tests/test_agent_metrics.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Run Promptfoo eval
        run: |
          npx promptfoo@latest eval -c promptfooconfig.yaml -o results.json
          FAILURES=$(python -c "import json; print(json.load(open('results.json'))['results']['stats']['failures'])")
          if [ "$FAILURES" -gt 0 ]; then
            echo "REGRESSION: $FAILURES test cases failed"
            exit 1
          fi
```

### Best Practices

- **Cache evaluations** to reduce API costs on unchanged tests.
- **Version-control prompts** alongside code -- treat them as first-class artifacts.
- **Path filtering:** Only trigger evals when prompt/agent/tool files change.
- **Store eval results** as build artifacts for team review and trend analysis.
- **Start read-only:** Give [[AGENTS|agents]] triage/analysis roles before write access.

---

## 10. Keystone-Specific Implementation Recommendations

Based on this research, here is a concrete action plan for the Keystone agent system:

### Phase 1: Foundation (Week 1-2)
- Install DeepEval (`pip install deepeval`) and set up pytest integration.
- Create a `tests/agent/` directory with mock tool fixtures.
- Build 20 "golden" test cases from real Keystone agent traces covering: brain search, tool multiplexing, file operations, and web research.

### Phase 2: Property Tests (Week 3)
- Install Hypothesis (`pip install hypothesis`).
- Define 10 core invariants (safety rules, tool routing rules, parameter validation).
- Set up snapshot baseline for critical agent workflows.

### Phase 3: CI/CD Integration (Week 4)
- Add evaluation gates to the deployment pipeline.
- Configure Promptfoo YAML for prompt regression testing.
- Set up drift detection alerts for production agent behavior.

### Phase 4: Self-Learning Loop (Ongoing)
- Auto-generate test cases from production traces weekly.
- Track improvement metrics in a dashboard.
- Feed failure cases back into the test suite automatically.

---

## Key Tools to Install

```bash
pip install deepeval hypothesis pytest-asyncio langsmith
npm install -g promptfoo
pip install ragas  # If using RAG pipelines
pip install langfuse  # For production observability
```

---

## Sources Consulted

- DeepEval documentation and GitHub (2025)
- Promptfoo CI/CD integration guides (2025)
- Maxim AI agent simulation platform docs
- Arize Phoenix observability documentation
- LangSmith evaluation templates (LangChain)
- Hypothesis library documentation (Python PBT)
- NVIDIA HEPH automated testing framework research
- Openlayer agent evaluation platform
- Multiple Reddit threads on AI agent testing strategies (r/MachineLearning, r/LangChain)
- Industry reports on CI/CD for AI [[AGENTS|agents]] (JetBrains, Cresta, Braintrust)
- OWASP/NIST frameworks for AI agent security testing
- Academic papers on agent trajectory evaluation (arXiv, 2024-2025)


---
📁 **See also:** ← Directory Index
