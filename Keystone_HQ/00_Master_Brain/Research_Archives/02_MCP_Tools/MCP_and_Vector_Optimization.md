# Architecting Cost-Efficient Autonomous Agent Systems

## 1. The Model Context Protocol (MCP) and Transport Upgrades
- **Deprecation of HTTP+SSE:** The legacy two-endpoint model (HTTP for POST, SSE for streams) is deprecated due to [[STATE|state]] correlation issues, load balancing friction, and DNS rebinding vulnerabilities.
- **Streamable HTTP:** The modern standard uses a unified `/mcp` endpoint supporting both POST and GET, natively supporting streaming over a single connection.
- **JSON-RPC 2.0:** All communication is standardized, strictly using `Mcp-Session-Id` headers for stateless routing across enterprise gateways.

## 2. Provider-Specific Prompt Caching Strategies
To dramatically reduce API costs and token burn, caching is mandatory for large static contexts (e.g., system prompts, tools).

### Anthropic Claude (Ephemeral Caching)
- Uses `cache_control` blocks with exact prefix matching.
- **Pricing:** 1.25x - 2.0x base rate to write cache (5-min vs 1-hour TTL). 90% discount (0.1x base rate) on cache hits.
- **Mechanics:** Modifying tools or early prompt layers invalidates the cache. Prefix must be sequentially ordered: Tools -> System Prompt -> User/Assistant logs.

### Google Gemini (Implicit & Explicit Caching)
- **Implicit Caching:** Automatic on Gemini 2.5/3.5 for stable prefixes >1024 tokens. No SLA.
- **Explicit Caching:** Requires calling the `/cachedContents` REST endpoint. Generates a durable resource name. Ideal for massive, stable tool definitions. Costs hourly storage ($1-$4.50/M tokens/hr).

## 3. Dynamic Context Pruning (DYCP) & KadaneDial
Continuous conversational logs create massive "log bloat", inflating costs and causing "Lost in the Middle" degradation.
- **KadaneDial Algorithm:** Transforms dialog history into dense vector embeddings, scoring relevance against the immediate query.
- Identifies **contiguous spans** of high-relevance history (score > 0.6) and concatenates them chronologically, stripping out irrelevant console dumps and stale outputs before sending the payload to the LLM.

## 4. Intent Routing Gateways
- **Single Orchestration Node:** A high-speed, cheap classifier (e.g., Gemini 2.5 Flash) analyzes incoming queries to determine intent and required depth.
- **Tiered Model Registry:** 
  - Routine tasks/JSON formatting -> Cheap models (Flash/Haiku).
  - Deep reasoning/Architecture -> Premium models (Sonnet/Opus).

## 5. Local Vector Database Optimization (Sub-10ms Agent Retrieval)
- **The 10ms Imperative:** Remote vector databases (150-500ms latency) throttle agent loops. Local optimizations are strictly required.
- **Hybrid Search Model:** Combine SQLite Full-Text Search 5 (FTS5) for exact lexical matching with high-dimensional vector embeddings for semantic approximation natively on the filesystem.
- **Layout-Aware Chunking:** Moving beyond naive token-splitting to parsing structural layouts maps perfectly to high-speed recall.


---
📁 **See also:** ← Directory Index

**Related:** [[20260613_AGENT_ARCH_qdrant_vector_database_advanced_optimization_for_ai_agent_me]] · [[01_Vector_DB_Optimization]]
