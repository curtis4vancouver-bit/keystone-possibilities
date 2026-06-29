# DEEP RESEARCH PROMPTS: ADA, VECTOR BRAIN, & NPC INTEGRATION

This file contains the 4 master prompts designed to trigger Google Gemini Deep Research sweeps for our framework upgrades.

---

## PROMPT 1 — AgentAda & Skill-Adaptive Data Analytics

```text
Perform an exhaustive, production-grade technical analysis of the AgentAda framework (arXiv:2504.07421) and skill-adaptive data analytics architectures. 

Your report must cover the following core areas:
1. Architectural Blueprint: Detail the end-to-end dataset-to-insight pipeline, explaining the specific roles of the Question Generator, the Hybrid RAG Skill Matcher, and the Code Generator.
2. Skill Library Design: How are analytical skills structured, documented, and exposed to the agent? Detail the metadata required for dynamic skill selection and how to prevent schema drift.
3. Execution and Security: Analyze the code generation execution loop. What sandboxing techniques, runtime verifications, and state management practices ensure that generated Python/SQL code executes safely?
4. Evaluation Frameworks: Analyze the KaggleBench benchmark and the LLM-as-a-judge methodologies for evaluating the quality of extracted insights. How can we implement this at scale for our own multi-agent fleet?

Provide concrete, copy-pasteable Python and prompt-template examples illustrating the skill-matching and execution wrapper classes.
```

---

## PROMPT 2 — AI NPCs & Persistent Agent Systems (npcpy & incognide)

```text
Perform a comprehensive technical analysis of npcpy, npcsh (NPC Shell), and the incognide desktop application for building persistent, state-aware AI NPCs.

Your report must cover the following core areas:
1. Local Database & State Management: Analyze how npcpy uses local SQLite databases (~/npcsh_history.db) to record user sessions, track NPC states, and auto-derive conversational knowledge graphs.
2. Jinja Execution Templates (Jinxes): What is the schema and runtime mechanics of Jinxes? How do agents and users share and execute these templates?
3. Progressive Skill Disclosure: Detail the mechanism by which npcpy/incognide loads skills. How does it prevent context window token bloat by dynamically loading only relevant skill segments?
4. Episodic Memory & Knowledge Graph Integration: Explain the integration of vector brains (SQLite-vec / Qdrant) with relational knowledge graphs. How do NPCs retrieve long-term context without losing situational awareness?

Provide sample code showing how to define an NPC, a Jinx, and a skill file matching the npcpy/incognide specifications.
```

---

## PROMPT 3 — Enterprise Browser Automation & Google Flow CDP Integration

```text
Perform a deep systems engineering analysis of automating complex React/Jotai SPAs (specifically Google Flow at labs.google/fx/tools/flow) using Chrome DevTools Protocol (CDP) and Playwright.

Your report must cover the following core areas:
1. DOM vs. CDP Input Simulation: Detail the exact mechanisms for simulating mouse clicks and keyboard typing to trigger React's synthetic event handler, avoiding Virtual DOM desyncs.
2. Jotai State Syncing: How do we inspect and preserve Jotai atomic store values (such as character likeness, environment anchors, and aspect ratios) across batch submissions?
3. Queue Management & Rate Limiting: Design a state machine to manage concurrent video/image generation queues in Google Flow. How do we prevent UI timeouts, handle generation failures, and optimize credit burn?
4. Persistent Visual References: Analyze how to programmatically pass Subject, Style, and Environment image references to Veo 3.1 via browser automation inputs.

Provide Python/Playwright snippets showing how to click, type, and intercept state changes on a Jotai-backed UI.
```

---

## PROMPT 4 — Code as Agent Harness & Paper2Code Architectures

```text
Perform an in-depth analysis of "Code as Agent Harness" (arXiv:2605.18747) and "Paper2Code" (e.g., PaperCoder, paper2code repositories) agent systems.

Your report must cover the following core areas:
1. Operational Harnessing: Detail the concept of code acting as the operational substrate for agent reasoning, acting, and self-verification. How does this compare to traditional scaffolding (ReAct)?
2. Paper-to-Code Pipeline: Break down the stages of transforming scientific papers (arXiv URLs) into modular, dependency-aware operational code repos. What roles do the planning, analysis, and generation stages play?
3. Collaborative Data Visualization (CoDA): Explain multi-agent collaboration for planning, visualization generation, and self-reflection loops.
4. Framework Upgrades: How can we leverage these concepts to build a self-evolving skill compiler that automatically translates new AI research papers into native skills for our agent fleet?

Provide architectural diagrams (represented in Mermaid) and prompt-flow schemas for the paper-to-code compiler.
```
