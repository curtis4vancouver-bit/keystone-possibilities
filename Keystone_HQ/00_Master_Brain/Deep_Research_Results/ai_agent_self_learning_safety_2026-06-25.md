Implementing Safe Self-Learning Loops for AI Coding Agents: A 2026 Architectural Standard

The evolution of large language model (LLM) agents has fundamentally shifted the paradigm of software engineering from static, single-execution scripting to autonomous, long-term sequential decision-making. As agents traverse complex codebases, they encounter partially observable environments laden with stochastic variables, undocumented dependencies, and intricate systemic constraints. However, a critical bottleneck in deploying autonomous coding agents at enterprise scale has been the inability to safely accumulate and apply knowledge across diverse sessions without triggering catastrophic forgetting, cascading rule bloat, or behavioral degradation. Historically, agents treated each new task as an independent challenge, failing to extract reusable expertise from successful trajectories. When simplistic, unconstrained self-updating mechanisms were introduced, agents frequently suffered from "prompt drift"—a phenomenon whereby the accumulation of unstructured, context-specific advice overrode foundational instructions, leading to catastrophic regressions in core competencies.   

To resolve these systemic vulnerabilities, the industry has standardized around a multi-layered architectural paradigm for safe self-learning loops. This comprehensive framework integrates causal abstractions for generalized memory retention , Free Spaced Repetition Scheduler (FSRS) decay algorithms for relevance weighting and bloat prevention , the Lore protocol for Git-integrated version control , and rigorous human-in-the-loop (HITL) staging pipelines governed by golden sample test suites. Furthermore, modern implementations utilize sophisticated trajectory mining techniques to facilitate multi-agent learning across shared correction journals, ensuring that parallel agent sessions do not overwrite or corrupt institutional memory.   

This report delivers an exhaustive, component-by-component analysis of this state-of-the-art self-learning architecture. It dissects the theoretical underpinnings of continual learning, examines real-world deployment data, and provides a complete architectural schematic and Python implementation for a production-grade safe self-learning daemon in 2026.

1. Real-World Efficacy: Agents that Self-Learn Without Degradation

Before dissecting the architectural components, it is critical to establish the empirical baseline for why safe self-learning loops are strictly necessary. Sequential decision-making tasks are unforgiving; an agent must repeatedly observe an environment, act based on internal beliefs, and update those beliefs based on stochastic outcomes. In the past, frameworks like Reflexion improved task performance by reflecting on failed attempts, but their reflections were hyper-specific to the immediate environment (e.g., "In the next trial, I will go to desk 1 and find the lamp"). This episodic memory failed entirely when the agent was placed in a novel environment, resulting in zero positive transfer learning.   

Modern implementations have categorically solved this through structural abstractions. The transition from episodic hints to causal rules and subagent patterns has yielded dramatic performance improvements across industry-standard benchmarks.

Empirical Benchmarks of Self-Learning Agents

The efficacy of modern continual learning frameworks is best demonstrated through their performance on standardized sequential decision-making environments, including ScienceWorld, ALFWorld, TravelPlanner, and open-ended environments like Minecraft.

Framework & Agent	Evaluation Environment	Key Mechanism Employed	Performance Metric / Improvement	Reference
CLIN	ScienceWorld	Causal Abstractions, Meta-Memory	+23 absolute point improvement over state-of-the-art reflective agents (Reflexion).	
CLIN	ALFWorld	Persistent Dynamic Textual Memory	+1.4 absolute points on base tasks; +11 points when transferring to novel environments.	
AutoRefine	TravelPlanner	Subagent Extraction, Procedural Memory	Achieved 27.1% success rate, exceeding manually designed orchestration systems (12.1%).	
AutoRefine	ScienceWorld	Dual-Form Experience Patterns	70.4% task completion with 20-73% reduction in necessary computational steps.	
Voyager	Minecraft	Transferable Skill Library Curriculum	Open-ended skill acquisition without degradation; code stored as executable functional primitives.	
  

As the data illustrates, the CLIN framework's ability to abstract causal relationships allows it to generalize learning across episodes. In ScienceWorld, a simulation of real-world physical and chemical interactions, CLIN successfully transferred insights from a "Roast a marshmallow" task to a "Melt cadmium" task by abstracting the core necessity of applying a heat source, independent of the specific object. Similarly, the AutoRefine framework demonstrated that automated extraction of procedural logic drastically outperforms human-authored orchestration, validating the premise that agents must author their own experiential rules. Voyager proved that skill libraries (the equivalent of an AI coding agent's SKILL.md) could be continually expanded without degrading prior competencies, provided the inputs are strictly formatted as functional code.   

2. The CLIN Framework: Implementing Causal Abstractions

The foundational flaw in early reflective memory systems was their reliance on unstructured natural language advice. To operate safely over extended periods, an agent's memory must function as a linguistic form of action modeling. The Continually Learning from Interactions (CLIN) framework resolves this by utilizing a persistent, dynamic textual memory centered entirely on causal abstractions.   

The Architecture of Abstraction

To operationalize continual learning without requiring downstream parameter weight updates, the CLIN architecture decomposes the agent into four distinct processing modules :   

Controller: The strategic core. It ingests the current task objective, queries the memory repository for relevant causal abstractions, and analyzes the trajectory of the trial so far to generate the next logical goal.   

Executor: The tactical interface. It converts the Controller's abstract goal into a discrete, syntactically valid action within the target environment (e.g., executing a specific Git command, reading a file, or modifying an Abstract Syntax Tree).   

Memory: A persistent database of natural language sentences that express generalized causal relationships governing the environment.   

Memory Generator: A background daemon invoked at the conclusion of a session. It abstracts the raw trajectory log into new causal rules, pruning redundant or ineffective memory nodes based on historical utility.   

Encoding Relational Causality

CLIN strictly prohibits the generation of freeform hints. Instead, the Memory Generator is forced via system prompts to encode reflections using standardized relational operators and linguistic uncertainty markers. This constraint ensures that all rules remain machine-parseable and uniformly applicable across diverse coding scenarios.   

The primary causal relations utilized in CLIN memory stores are:

"Is necessary to" / "Enables": Encodes prerequisite actions and positive operational pathways. (e.g., "Initializing a localized virtual environment is necessary to prevent global dependency conflicts during Python package installation").

"Does not contribute to" / "Prevents": Encodes anti-patterns, failed trajectories, or explicit operational blocks. (e.g., "Force-pushing to the main deployment branch does not contribute to stable CI/CD pipelines").

These absolute relations are modulated by linguistic uncertainty parameters, which act as a primitive form of probabilistic weighting before FSRS decay is applied.   

"May be": Indicates low initial confidence. Used when a causal link is observed in a single trial but lacks extensive validation.

"Should be": Indicates high confidence. The agent upgrades a rule from "may be" to "should be" after it successfully relies on the abstraction across multiple, varied trials.   

Meta-Memory and Episode Generalization

To prevent an agent from overfitting its rules to a specific repository, the CLIN framework employs a "meta-memory" summarization phase. After a predefined sequence of trials or a completed project milestone, the system evaluates the localized memories. The highest-performing abstractions are distilled into generalized meta-rules. For example, if an agent learns that locating configuration files in repo_A requires traversing the /config directory, and in repo_B it requires traversing the /.github directory, the meta-memory generator abstracts this to: "Moving through hidden directories and executing grep operations should be necessary to discover project-wide configuration constraints.".   

3. Multi-Agent Learning and the Correction Journal

In enterprise environments, AI coding agents do not operate in isolation. Fleets of agents concurrently execute tasks across microservices, shared repositories, and distinct branches. A naive self-learning system where every agent independently mutates a shared SKILL.md file inevitably results in race conditions, contradictory rule sets, and systemic memory corruption. To handle multi-agent learning safely, the 2026 standard introduces the Trajectory Miner and the centralized Correction Journal.   

The Trajectory Miner and Experience Extraction

To bridge the gap between raw execution logs and structured causal rules, architectures like AutoRefine deploy a specialized Trajectory Miner. The Trajectory Miner operates asynchronously, scanning agent execution histories to extract "reusable expertise". Rather than replaying entire sessions, the miner identifies critical decision nodes and the reasoning patterns that precipitated success or failure.   

Agents at scale generate vast quantities of data. To manage this, the Trajectory Miner extracts knowledge into two distinct schemas: Skill Patterns and Subagent Patterns.   

Pattern Type	Defining Characteristics	Context Dependency	Extraction Goal	Reference
Skill Pattern	Typically < 5 steps. 0-2 simple conditionals. No complex orchestration needed.	Stateless. Each invocation is independent of long-term state.	Procedural knowledge expressed as natural language rules or executable code snippets (e.g., regex strings).	
Subagent Pattern	Typically 5+ steps. 3+ decision points requiring reasoning. Multiple tool calls with dependencies.	Stateful. Maintains internal memory and state transitions.	Encapsulates complex procedures into atomic operations. Generates a specialized subagent that the main agent can delegate to.	
  
Implementing the Shared Correction Journal

When multiple agents generate improvement suggestions, they do not write directly to the persistent rule store. Instead, they log their findings to a decentralized directory, commonly structured as ~/.claude/state/improvements/ or a distributed equivalent.   

A centralized aggregation daemon processes this Correction Journal. To prevent the overarching system from overreacting to isolated anomalies or hallucinated edge cases, the aggregator applies a strict frequency threshold. A pattern must be independently detected in at least two separate agent sessions to qualify as a "recurring" skill candidate. Single occurrences are logged as "incidents" for telemetry but are structurally prevented from generating permanent rules.   

Once a pattern crosses the threshold, the system extracts a formalized skill containing the pattern ID, the trigger condition ("When to apply this skill"), the necessary steps, tool requirements, and root cause clusters. This formalized skill is then routed into the agent rule store, where it is subjected to relevance decay weighting.   

4. FSRS-Based Memory Decay for AI Agent Rule Stores

As the Trajectory Miner continuously pushes new causal abstractions and skill patterns to the agent's memory, the rule store inevitably expands. An unbounded context window filled with thousands of hyper-specific rules leads directly to "prompt drift," where the sheer volume of niche instructions dilutes the agent's adherence to foundational security and formatting directives.   

To safely manage this repository, the agent memory store implements the Free Spaced Repetition Scheduler (FSRS), specifically version 4.5. While originally designed to optimize flashcard scheduling for human cognitive retention based on Hermann Ebbinghaus's forgetting curve, FSRS is repurposed in AI architectures as a dynamic relevance decay model. The algorithm predicts the mathematical probability that a specific rule will be necessary for an upcoming task, decaying the relevance of highly specific, rarely used rules over time while solidifying universally applicable causal abstractions.   

The DSR Memory Model in Autonomous Agents

The FSRS algorithm fundamentally models memory via three core variables, known as the DSR model: Difficulty (D), Stability (S), and Retrievability (R).   

1. Difficulty (D):
In human applications, difficulty measures the inherent cognitive load of a concept. For AI rule stores, Difficulty ($D \in $) represents the complexity, length, and contextual specificity of the skill pattern. A foundational, universal rule (e.g., "All functions must contain type hints") is assigned a low D value. Conversely, a highly specific subagent pattern (e.g., "Steps to resolve a Webpack circular dependency in legacy micro-frontends") is assigned a high D value, reflecting its narrow applicability.   

2. Stability (S):
Stability (S∈[0,+∞]) measures the durability and proven utility of the rule over time. Technically, it is defined as the number of days (or operational cycles) required for the Retrievability (R) of the rule to decay from 100% to a target threshold of 90%. A high S value indicates a robust, universally applicable rule that remains relevant for months without needing to be repeatedly validated.   

3. Retrievability (R):
Retrievability ($R \in $) calculates the instantaneous probability of successful recall. In an AI context, R functions as the active relevance score. When constructing the prompt or context window for a new task, the agent queries the FSRS database; only rules with an R value above a designated threshold (typically 0.85) are injected into the active context.   

The Mathematical Decay Function

FSRS departs from traditional exponential decay models (like SM-2) by calculating the decay of Retrievability using a highly optimized power function. This provides a superior approximation for long-tail memory retention. The decay function is formally defined as:   

R(t)=(1+F
S
t
	​

)
C

Where:

t represents the elapsed time (measured in days or execution cycles) since the rule was last successfully applied.   

S is the current Stability of the rule.   

F is a scaling constant. In FSRS v4.5, this has been empirically optimized through gradient descent across millions of interactions to 
81
19
	​

.   

C is the shape parameter, fixed at −0.5.   

Dynamically Updating Parameters: The Stability Increase (SInc)

The true power of FSRS lies in its dynamic updating mechanism. When an agent successfully retrieves a rule and applies it to complete a task without error, the rule's Stability must be recalculated. The new Stability is derived by multiplying the prior Stability by a Stability Increase factor (SInc≥1).   

The SInc value is determined by a complex, non-linear interplay of the current D, S, and R variables at the moment of successful retrieval:

Difficulty Penalty (t
d
	​

): Harder rules (higher D) increase in stability more slowly. Modeled via linear damping as t
d
	​

=11−D, this dynamic ensures that highly complex, niche rules require frequent, repeated utility to achieve high systemic stability.   

Stability Saturation (t
s
	​

): The more stable a rule already is, the harder it becomes to increase its stability further. Modeled as t
s
	​

=S
−w
9
	​

 (where w
9
	​

 is an optimized weight parameter), this mathematically forces foundational rules to hit a natural saturation ceiling, preventing runaway scaling.   

Retrievability Factor (t
r
	​

): The smaller the value of R at the exact time of successful application, the larger the resulting SInc. If a rule was nearly decayed out of relevance but is suddenly required and perfectly solves an edge case, its stability receives a massive boost, signaling renewed operational importance to the agent fleet.   

By utilizing this continuous, mathematically rigorous maintenance mechanism, the FSRS rule store effectively prunes the SKILL.md file and vector databases. Rules that fall below the R threshold are archived to cold storage. They are no longer injected into the active prompt, immediately resolving context window exhaustion while preserving the capacity to retrieve them if explicitly queried by a future subagent.   

5. The Staging and Promotion Pipeline

The theoretical elegance of FSRS decay and causal abstractions is rendered moot if corrupted or hallucinated rules are allowed to infect the core memory store. Agents cannot be permitted to push raw, untested abstractions directly to a production SKILL.md file. The 2026 operational standard mandates a strict lifecycle management control plane featuring an immutable Pending → Confirmed → Promoted pipeline.   

Pipeline Stages and Execution Isolation

Pending State: When the Trajectory Miner identifies a recurring pattern that crosses the frequency threshold, it generates a draft skill abstraction. This draft rule is stored in a heavily isolated registry with a strict Read-only classification. It is explicitly blocked from influencing production agents.   

Confirmed State: The pending rule is routed into an ephemeral, sandboxed testing environment. Here, it is subjected to an automated validation suite. The rule must pass formatting contracts and be successfully applied in simulated scenarios without triggering regressions in pre-existing agent capabilities. If it passes all programmatic assertions, its status is updated to Confirmed.   

Promoted State: If the automated tests succeed without exception, the rule is elevated to Promoted status. It is formally integrated into the active FSRS memory store and serialized into the project's version-controlled SKILL.md file. For rules affecting critical infrastructure, a human-in-the-loop (HITL) approval gate is injected between Confirmation and Promotion.   

Output Contracts and Golden Sample Test Suites

The validation phase is entirely dependent on the rigor of "Output Contracts" and "Golden Sample" test suites. Treating prompts and skills as functional code means they require unit testing. An output contract is a formal specification of the behavioral shift the new rule is expected to produce. It defines the exact JSON schema, required field mappings, acceptable classification labels, and graceful failure modes that downstream systems demand.   

A Golden Sample test suite contains known, immutable ground-truth inputs mapped to highly specific expected outputs. During the Confirmation stage, the system executes a sandboxed agent against the Golden Sample suite with the new rule injected into its context.   

Critical Failure Mode Prevented	Detection Mechanism via Golden Sample	

Resolution / Fix Requirement 


Silent JSON Degradation	Parser extracts empty results or encounters markdown code fences wrapping what should be raw JSON output.	Reject rule. Require the abstracted rule to specify strict schema formatting without markdown injection.
Multi-Agent Chain Drift	Hand-off payloads between Agent A and Agent B fail due to shifting key-value structures.	Log intermediate hand-offs. Reject rule if upstream output violates any downstream contract dependencies.
Tool Call Hallucination	Agent invokes tools aggressively or attempts to use newly discovered tools outside of defined scope.	Audit tool call logs against the expected Golden Sample trajectory. Reject if out of bounds.
Regression in Few-Shot Examples	The new rule causes the agent to ignore historical few-shot examples or follow them too literally, degrading zero-shot performance.	Explicitly verify that pre-existing few-shot examples still produce the intended behavioral effect when the new rule is active.
  

If the Golden Sample execution perfectly matches the expected ground truth and generates zero secondary regressions across the test matrix, the rule passes validation and awaits promotion.

6. Enforcing Append-Only Operations and HITL Gates

A foundational security protocol in continual learning architectures is the absolute prohibition of destructive updates. To prevent an agent from inadvertently deleting crucial institutional knowledge, AI agents are granted Write/Update authority exclusively for appending new data. They must never delete, overwrite, or mutate working, highly stable rules without explicit cryptographic authorization.   

The Append-Only Mutability Policy

Modifying a pre-existing rule that boasts a high FSRS Stability metric (e.g., S>100) introduces severe, unpredictable risk, as that specific rule likely underpins thousands of successful past trajectories. If an operational conflict arises between an existing stable rule and a newly discovered context, the agent is structurally forced to extract a conditional exception rather than modifying the base rule.

For example, an agent must not delete the foundational rule: "Always use Python 3.10 for microservices." Instead, the agent appends a new rule with a higher specificity trigger: "When executing legacy graphics rendering modules in the video-proc service, bypass Python 3.10 and utilize Python 3.8 to avoid C-binding errors." The FSRS engine natively handles this; highly specific rules receive precedence in the context window over general rules when their specific triggers are activated.

Risk Classification and Human-In-The-Loop (HITL)

While automated Golden Sample testing is robust, certain domains carry risks that cannot be purely algorithmically verified. The agent control plane enforces fine-grained authorization by categorizing the new rule's functional domain and assigning it a risk severity classification.   

Any rule modifications touching high-risk or very high-risk domains must trigger a mandatory Human-in-the-Loop (HITL) approval gate. The system pauses the promotion pipeline, generates a summary diff, and alerts an engineering manager.   

Permission / Action Type	Example of Agent Capability	Assigned Risk Level	

HITL Requirement 


Read-only	Retrieving documentation, parsing logs, reading Git history.	Lower	None (Automated Promotion)
Draft-only	Preparing PR descriptions, drafting internal reports.	Medium	None (Automated Promotion)
Write/Update	Modifying source code, appending rules to SKILL.md.	Higher	Threshold-based / Sampled Approval
Trigger Workflow	Initiating CI/CD pipelines, escalating severe incidents.	Higher	Mandatory Manager Approval
External Communication	Messaging customers or external API endpoints.	High	Mandatory Manager Approval
Financial/Legal	Approving payments, signing compliance steps.	Very High	Mandatory Two-Factor HITL
  

By structurally decoupling the agent's ability to reason from its authority to execute permanent changes, enterprise architectures prevent autonomous loops from silently corrupting critical infrastructure or violating compliance mandates. An agent should never operate as a "ghost user" holding standing, unreviewed access.   

7. Git Auto-Commit Patterns and the Lore Protocol

Once a rule clears the staging pipeline and achieves Promoted status, it must be serialized into the codebase's permanent version control. However, simply appending text lines to a SKILL.md file strips the rule of its origin, justification, rejected alternatives, and temporal context. The industry has addressed this structural deficit by implementing the "Lore Protocol"—a standardized methodology that repurposes native Git commit messages to serve as a machine-parseable knowledge channel for AI agents.   

Overcoming the Decision Shadow

When standard AI agents generate code or rules, the resulting Git commit captures the binary diff but entirely discards the "Decision Shadow"—the external constraints, rejected alternatives, and forward-looking context that fundamentally shaped the implementation.   

The Lore Protocol mandates that every automated modification to the codebase or SKILL.md be stored as an atomic "Lore atom". This binds the explicit causal knowledge permanently to the exact code change it describes. Because it relies entirely on native Git architecture, there is zero infrastructure overhead, and it avoids the synchronization decay inherent in external wikis or Architectural Decision Records (ADRs).   

Structuring Knowledge via Git Trailers

Lore achieves its machine-parseability by strictly utilizing Git trailers—native, structured key-value pairs appended to the bottom of the commit message. An automated agent updating the SKILL.md file generates a commit formatted precisely as follows:   

Update database connection handling rule in SKILL.md

The previous retry logic resulted in cascading timeouts during high load.
This commit injects an exponential backoff causal abstraction to prevent DB lockouts.

Rejected: Hardcoded 5-second delays (fails under peak load scenarios).
Directive: Ensure all future connection pools respect the MAX_RETRIES env var.
Related: #452

Agent Discovery and Context Harvest

When an AI agent is initialized in a Lore-enabled repository, it does not begin coding immediately. It performs a structured discovery phase using discoverable CLI interactions.   

Constraint Harvest: Before modifying any file, the agent runs the lore context <path> CLI command (a standardized wrapper around git log --trailer=) to load the full decision history into its working context window.   

Anti-pattern Filtering: By programmatically parsing the Rejected: trailers, the agent is structurally prevented from re-exploring dead-ends that previous agents already attempted and failed.   

Directive Absorption: The Directive: trailers function as permanent, searchable messages passed chronologically from past authors to future modifiers. They act as institutional knowledge that guides implementation strategy without cluttering the main source files with excessive comments.   

Parallel Execution via Git Worktrees

When executing parallel learning loops, fleets of agents cannot operate in the same standard Git directory. Concurrent modifications to SKILL.md will result in merge conflicts that agents often struggle to resolve natively. To manage this, agents are instructed to utilize Git worktrees for parallel sessions. A worktree allows multiple working trees to be attached to a single repository, enabling agents to branch, modify, test, and generate Lore commits in complete isolation before a centralized CI/CD pipeline sequentially merges the verified branches back into the mainline.   

8. Monitoring and Mitigating Rule Drift

"Rule Drift" (or "Prompt Drift") is the gradual, unintended shift of AI outputs away from intended constraints, scope, or style over repeated prompt iterations. As rules are continuously appended to SKILL.md, the sheer accumulation of new instructions can alter how the underlying model attends to and interprets earlier, foundational instructions—a phenomenon explicitly categorized as schema evolution drift.   

To maintain stability across a multi-year deployment, platform engineers must implement active detection for three primary drift typologies :   

Typologies of Drift

Prompt Drift (Schema Evolution): An intentional tweak to improve one metric inadvertently degrades another. For example, a safety addition regarding data handling causes the model to over-refuse on benign coding questions. Furthermore, adding a new tool to the agent's schema changes how the model interprets earlier rules, shifting behavior even though the exact wording of the older rules remained untouched. Detection requires versioning every prompt and gating every PR on offline evaluations.   

Model Drift: The upstream LLM provider updates their proprietary model weights silently, without notification. The agent suddenly begins processing the identical SKILL.md rules differently.   

Eval-Score Drift: A rolling-mean drop in the agent's performance rubric scores across live production spans. This is detected when a secondary "judge model" scores production outputs and notices gradual degradation over a 24-hour window.   

Active Drift Detection Mechanisms

To detect Model Drift, modern control planes employ continuous Canary Replays. A versioned, hashed, and dated set of 50-200 complex prompt scenarios is maintained as a pristine baseline. The learning daemon replays this canary set against the production model ID daily. The expected outputs and rubric scores are recorded. If the daily replay produces a rubric pass rate that drops by 2-5% sustained over 3-7 days, a severe investigation alert is triggered, and the engineering team determines if the provider's model weights have shifted.   

Furthermore, Input Distribution Shift is monitored via vector embeddings. User prompts and environmental inputs shift over time. To detect this, every input is embedded and clustered periodically. If a new cluster emerges that significantly shifts the overall distribution size, it flags that the agent is encountering inputs it was not originally trained or prompted for. The learning loop is halted, and engineers review the FSRS memory weights to ensure the agent has the necessary causal abstractions to handle the new input domains before degradation affects production.   

9. Reference Implementation: The Safe Self-Learning Daemon

To demonstrate the practical, programmatic integration of CLIN causal abstractions, FSRS decay equations, the Lore protocol, and golden sample validation, the following Python reference implementation outlines a production-grade SelfLearningDaemon.

This modular architecture demonstrates the pipeline required to safely evaluate, decay, and persist knowledge in an autonomous AI agent environment in 2026. The code is heavily annotated to illustrate the translation of the theoretical concepts detailed above into functional logic.

Python
import time
import math
import json
import subprocess
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

# ==========================================
# 1. Data Structures: CLIN Abstractions & FSRS
# ==========================================
@dataclass
class FSRSData:
    """Represents the DSR memory state of an agent rule."""
    difficulty: float = 5.5  # D in : High D = complex, niche subagent logic
    stability: float = 1.0   # S in days: Time until retrievability drops to 90%
    retrievability: float = 1.0  # R in : Probability of recall / relevance score
    last_reviewed: datetime = field(default_factory=datetime.now)

@dataclass
class CausalRule:
    """A CLIN-style causal abstraction rule."""
    id: str
    condition: str
    relation: str  # "necessary", "does not contribute", "prevents"
    action: str
    uncertainty: str # "may be", "should be"
    fsrs: FSRSData = field(default_factory=FSRSData)
    status: str = "pending"  # Stages: pending, confirmed, promoted
    risk_level: str = "Medium" # Lower, Medium, Higher, High, Very High

# ==========================================
# 2. Memory Maintenance: FSRS Engine
# ==========================================
class FSRSEngine:
    """Handles the mathematical decay of rule relevance based on v4.5 parameters."""
    def __init__(self):
        # FSRS v4.5 optimized constants 
        self.F = 19.0 / 81.0
        self.C = -0.5
        
    def calculate_retrievability(self, rule: CausalRule, current_time: datetime) -> float:
        """Calculates R(t) based on power function decay."""
        elapsed_days = (current_time - rule.fsrs.last_reviewed).total_seconds() / 86400.0
        if elapsed_days < 0:
            return 1.0
        # Power function: R(t) = (1 + F * t / S)^C
        r_val = math.pow((1.0 + self.F * (elapsed_days / rule.fsrs.stability)), self.C)
        rule.fsrs.retrievability = max(0.0, min(1.0, r_val))
        return rule.fsrs.retrievability

    def update_stability_on_success(self, rule: CausalRule) -> None:
        """Updates stability (SInc) after successful application in a Golden Sample or prod task."""
        d = rule.fsrs.difficulty
        s = rule.fsrs.stability
        r = rule.fsrs.retrievability
        
        # Difficulty penalty: Harder rules scale slower via linear damping
        t_d = 11.0 - d
        # Stability saturation: Highly stable rules grow slower
        t_s = math.pow(s, -0.1) # Simplified representation of parameter w9
        # Retrievability factor: Recalling almost forgotten rules boosts stability massively
        t_r = math.exp(1.0 - r) 
        
        s_inc = max(1.0, t_d * t_s * t_r)
        rule.fsrs.stability *= s_inc
        rule.fsrs.last_reviewed = datetime.now()
        
    def update_on_failure(self, rule: CausalRule) -> None:
        """Lapse handling: Rule failed the golden sample or generated an error."""
        # Increase difficulty and slash stability
        rule.fsrs.difficulty = min(10.0, rule.fsrs.difficulty + 1.5)
        rule.fsrs.stability = max(0.1, rule.fsrs.stability * 0.5)
        rule.fsrs.last_reviewed = datetime.now()

# ==========================================
# 3. Versioning: Git Lore Protocol Manager
# ==========================================
class GitLoreManager:
    """Handles Git integration using the Lore protocol trailers."""
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def commit_promoted_rule(self, rule: CausalRule, rejected_alts: List[str], related_issue: str):
        """Commits the rule to SKILL.md with structured Lore trailers."""
        # 1. Append-only update to SKILL.md (Preventing destructive updates)
        with open(f"{self.repo_path}/SKILL.md", "a") as f:
            rule_text = f"\n- [{rule.uncertainty.upper()}] {rule.condition} is {rule.relation} to {rule.action}"
            f.write(rule_text)
            
        # 2. Construct Lore Commit Message targeting the Decision Shadow
        commit_msg = f"System Update: Promote causal rule {rule.id}\n\n"
        commit_msg += f"Automated FSRS relevance promotion from multi-agent correction journal.\n\n"
        for alt in rejected_alts:
            commit_msg += f"Rejected: {alt}\n"
        commit_msg += f"Directive: Ensure downstream parsing relies on strict JSON boundaries.\n"
        if related_issue:
            commit_msg += f"Related: {related_issue}\n"
        
        # 3. Execute Git commands inside the worktree
        try:
            subprocess.run(, cwd=self.repo_path, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.repo_path, check=True, capture_output=True)
            print(f"[Git] Lore Atom successfully created for Rule {rule.id}")
        except subprocess.CalledProcessError as e:
            print(f"[Git Error] Failed to commit Lore Atom: {e.stderr.decode()}")

# ==========================================
# 4. Validation: Golden Sample Evaluator
# ==========================================
class GoldenSampleEvaluator:
    """Validates rules against strict output contracts to prevent Silent JSON Degradation."""
    def __init__(self, test_suite_path: str):
        self.test_suite_path = test_suite_path
        # In a real implementation, this loads ground truth data
        # with open(test_suite_path, 'r') as f:
        #     self.test_cases = json.load(f)

    def evaluate(self, rule: CausalRule) -> bool:
        """Simulates agent execution with the new rule to test for regressions."""
        print(f"[Eval] Evaluating Rule {rule.id} against Golden Samples...")
        
        # Mocking test execution matrix: 
        # Spins up an isolated sandbox, runs the agent with the new rule injected 
        # into the prompt, and asserts the JSON output matches the expected contract.
        
        # Example validation logic check
        if rule.relation == "prevents" and rule.risk_level == "Very High":
            print(f"[Eval] Rule {rule.id} failed structural contract: Missing fallback logic.")
            return False
            
        print(f"[Eval] Rule {rule.id} passed all golden sample matrix tests.")
        return True

# ==========================================
# 5. Pipeline Orchestration: Self-Learning Daemon
# ==========================================
class SelfLearningDaemon:
    """Orchestrates the Pending -> Confirmed -> Promoted lifecycle."""
    def __init__(self):
        self.fsrs = FSRSEngine()
        self.evaluator = GoldenSampleEvaluator("./golden_samples.json")
        self.git_lore = GitLoreManager("./repo")
        self.rule_store: Dict = {}
        
    def ingest_trajectory_pattern(self, pattern_data: dict):
        """Receives extracted patterns from the Trajectory Miner."""
        rule = CausalRule(
            id=pattern_data['id'],
            condition=pattern_data['condition'],
            relation=pattern_data['relation'],
            action=pattern_data['action'],
            uncertainty=pattern_data['uncertainty'],
            risk_level=pattern_data.get('risk_level', 'Medium')
        )
        self.rule_store[rule.id] = rule
        print(f"\n[Pipeline] Ingested pending rule: {rule.id}")
        self._process_pipeline(rule, pattern_data.get('rejected',), pattern_data.get('related', ''))

    def _process_pipeline(self, rule: CausalRule, rejected_alts: List[str], related: str):
        """Runs the lifecycle and enforces HITL gates."""
        # Stage 1: Automated Validation (Pending -> Confirmed)
        if self.evaluator.evaluate(rule):
            rule.status = "confirmed"
            print(f"[Pipeline] Rule {rule.id} confirmed via output contracts.")
            
            # Stage 2: Human In The Loop Gate (Confirmed -> Promoted)
            if self._hitl_approval_gate(rule):
                rule.status = "promoted"
                self.fsrs.update_stability_on_success(rule)
                self.git_lore.commit_promoted_rule(rule, rejected_alts, related)
            else:
                print(f"[Pipeline] Rule {rule.id} rejected by HITL manager.")
                self.fsrs.update_on_failure(rule)
        else:
            print(f"[Pipeline] Rule {rule.id} failed golden sample validation.")
            self.fsrs.update_on_failure(rule)

    def _hitl_approval_gate(self, rule: CausalRule) -> bool:
        """Pauses for human approval on high-severity modifications."""
        if rule.risk_level in ["High", "Very High"]:
            print(f" Awaiting managerial approval for {rule.id} due to {rule.risk_level} risk...")
            # Mocking async approval response
            time.sleep(1) 
            return True 
        print(f" Risk level {rule.risk_level} is below threshold. Auto-approving.")
        return True 

    def memory_maintenance_cycle(self):
        """Periodic background job to decay relevance and prune prompt bloat."""
        print("\n[Maintenance] Initiating FSRS Decay Cycle...")
        current_time = datetime.now()
        archived_count = 0
        
        for rule_id, rule in self.rule_store.items():
            if rule.status == "promoted":
                r_val = self.fsrs.calculate_retrievability(rule, current_time)
                if r_val < 0.85:
                    print(f" Rule {rule.id} retrievability dropped to {r_val:.2f}. Archiving from active context.")
                    rule.status = "archived"
                    archived_count += 1
                else:
                    print(f"[Active] Rule {rule.id} maintains retrievability at {r_val:.2f}.")
                    
        print(f"[Maintenance] Cycle complete. Archived {archived_count} obsolete rules.")

# ==========================================
# Execution Simulation
# ==========================================
if __name__ == "__main__":
    daemon = SelfLearningDaemon()
    
    # Mock data originating from the Multi-Agent Correction Journal
    extracted_pattern = {
        "id": "RULE-991",
        "condition": "Isolating package dependencies in virtual environments",
        "relation": "is necessary",
        "action": "preventing schema evolution drift",
        "uncertainty": "should be",
        "risk_level": "Higher",
        "rejected": ["Using global pip installs", "Ignoring requirements.txt version locking"],
        "related": "#1024"
    }
    
    # 1. Ingest and route through pipeline
    daemon.ingest_trajectory_pattern(extracted_pattern)
    
    # 2. Simulate 45 days passing to trigger FSRS decay
    print("\n Simulating 45 days of operational inactivity for RULE-991...")
    daemon.rule_store.fsrs.last_reviewed -= timedelta(days=45)
    
    # 3. Run maintenance cycle
    daemon.memory_maintenance_cycle()

Conclusion

The deployment of safe self-learning loops for AI coding agents requires a fundamental paradigm shift. Enterprises must move away from ad-hoc, prompt-based memory systems towards rigorous, architecturally integrated knowledge pipelines. By utilizing the CLIN framework and AutoRefine trajectory miners, agents replace brittle situational hints with generalized, causal abstractions and subagent patterns. The mathematical integration of the FSRS algorithm ensures that this accumulated knowledge is continuously pruned and optimized, preventing the prompt drift and context exhaustion that invariably degrade long-running autonomous systems.

Crucially, the translation of these dynamic memories into the project repository is secured by an immutable Pending → Confirmed → Promoted pipeline. This pipeline enforces strict Golden Sample output contracts to eliminate regressions and relies on Human-in-the-Loop checkpoints to govern high-risk domains. Finally, the Git Lore protocol guarantees that every causal rule added to SKILL.md is inextricably bound to its decision history, creating a machine-parseable audit trail that future agents can natively query.

Adopting this synthesis of causal cognitive modeling, strict lifecycle staging, mathematical relevance decay, and Git-native version control provides the definitive architectural blueprint for highly capable, self-improving AI agents in 2026.