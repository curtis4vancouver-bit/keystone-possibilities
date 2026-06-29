# Optimal Embedding Chunk Size and Overlap for Technical Markdown Documents

**Research Date:** May 22, 2026
**Domain:** vector_brain_optimization
**Sources:** 10+ web searches across academic papers, industry benchmarks, framework documentation, and practitioner reports
**Applicability:** Keystone Sovereign Master Brain (sqlite-vec backed vector DB with ~1,158 chunks across 57 sources)

---

## Executive Summary

After extensive research across current (2025-2026) industry benchmarks, framework best practices, and academic literature, the optimal configuration for embedding technical markdown documents in our Keystone brain is:

- **Primary chunk size:** 512 tokens (~2,000 characters) with heading-aware boundaries
- **Overlap:** 10-15% (50-75 tokens) -- but only when using fixed-size splitting
- **Strategy:** Two-pass hybrid: MarkdownHeaderTextSplitter first, then RecursiveCharacterTextSplitter as fallback for oversized sections
- **Metadata enrichment:** Prepend document title + full header hierarchy path to each chunk before embedding

---

## 1. Chunk Size Analysis: The Trade-Off Matrix

Chunk size is the single most impactful parameter in a RAG pipeline. Research consistently shows it affects both retrieval precision and generation quality.

### Size Comparison Table

| Chunk Size | Precision | Context Richness | Embedding Quality | Best Use Case |
|:-----------|:----------|:-----------------|:------------------|:--------------|
| **128-256 tokens** | Very High | Low | Focused but fragile | Fact lookups, FAQ matching |
| **256-512 tokens** | High | Moderate | Sweet spot for most | Technical docs, API references |
| **512-1024 tokens** | Moderate | High | Good for narrative | Long-form guides, tutorials |
| **1024-2048 tokens** | Low | Very High | Signal dilution risk | Full section retrieval only |

### Key Findings

**512 tokens is the consensus starting point** for technical documentation. This aligns with the training characteristics of most embedding models (OpenAI text-embedding-3, Cohere embed-v3, and local models like all-MiniLM-L6-v2).

**Signal dilution** is the primary risk of large chunks. When a single embedding vector tries to represent 2,048 tokens covering multiple sub-topics, the vector becomes a "blurred average" that matches many queries weakly rather than the right query strongly. This directly increases hallucination risk because the LLM receives context that is only partially relevant.

**Chunks below 128 tokens** lack sufficient semantic weight. They produce embeddings that are too specific, leading to false-positive matches on superficial keyword similarity rather than meaningful semantic alignment.

### Recommendation for Keystone Brain

Target **400-512 tokens** per chunk for our technical markdown documents. Given that our brain currently holds ~1,158 chunks across 57 sources (averaging ~20 chunks per document), this size maintains manageable index density while preserving semantic coherence.

---

## 2. Chunk Overlap: When and How Much

### The 10-20% Rule

Industry consensus recommends **10-20% overlap** between adjacent chunks. For a 512-token chunk, this means 50-100 tokens of shared content at boundaries.

### Critical Nuance: Overlap Is Less Important with Structure-Aware Chunking

Recent 2026 benchmarking reveals an important finding: **overlap provides near-zero measurable benefit when using heading-aware or semantic chunking**. The reason is straightforward -- if you split at natural document boundaries (section headers, paragraph breaks), there is no mid-sentence fragmentation to bridge.

Overlap is most valuable when:
- Using fixed-size character splitting on unstructured text
- Documents contain dense, flowing prose without clear section breaks
- Code examples span natural break points

Overlap is unnecessary when:
- Splitting strictly on markdown headers (H1/H2/H3)
- Each chunk represents a complete, self-contained section
- Using semantic chunking that detects topic shifts

### Recommendation for Keystone Brain

Use **50-token overlap (10%)** only as a fallback when the RecursiveCharacterTextSplitter must sub-divide an oversized markdown section. When splitting directly on headers, set overlap to 0.

---

## 3. Heading-Aware Chunking for Markdown

This is the single most impactful strategy for our use case. Technical markdown documents have inherent structure that should drive the chunking logic.

### Two-Pass Strategy

**Pass 1: MarkdownHeaderTextSplitter** -- Split on H1, H2, and H3 boundaries. Each resulting chunk automatically receives metadata containing its full header path.

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False  # Keep headers in content for embedding context
)
header_chunks = markdown_splitter.split_text(markdown_document)
```

**Pass 2: RecursiveCharacterTextSplitter** -- For any section that exceeds 512 tokens after header splitting, apply recursive splitting with overlap.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len  # Or use a token counter
)

final_chunks = text_splitter.split_documents(header_chunks)
# split_documents preserves the header metadata from Pass 1
```

### Why This Works

- Sections under a single H3 heading typically represent a single coherent concept
- The header hierarchy provides automatic metadata (no LLM enrichment needed)
- Code blocks and tables are more likely to stay intact within section boundaries
- The recursive fallback handles edge cases where a single section is very long

---

## 4. Metadata Enrichment Strategies

Adding metadata to chunks before embedding dramatically improves retrieval precision.

### Contextual Chunk Headers (CCH)

The most effective low-cost enrichment is prepending the full header path to each chunk's content before embedding:

```
[Document: BC Contractor Tax Compliance]
[Section: CRA Obligations]
[Sub-section: GST/HST Filing Requirements]

Contractors earning over $30,000 annually must register for GST/HST...
```

This solves the "lost pronoun" problem where chunks contain references like "it" or "this process" without the noun they refer to.

### Metadata Fields to Store

| Field | Purpose | Storage |
|:------|:--------|:--------|
| `doc_title` | Source document identification | Metadata column |
| `header_path` | Full H1 > H2 > H3 hierarchy | Prepend to content + metadata |
| `doc_date` | Temporal relevance filtering | Metadata column |
| `domain` | Topic-area filtering (tax, legal, tech) | Metadata column |
| `chunk_index` | Ordering for context expansion | Metadata column |
| `total_chunks` | Document scope awareness | Metadata column |

### Advanced: Anthropic's Contextual Retrieval

For high-value documents, use an LLM to generate a 50-100 token "situating context" for each chunk. This is prepended before embedding:

```
"This chunk is from the BC Contractor Tax Compliance guide, specifically
discussing quarterly GST/HST filing deadlines and penalties for late
submission. The document covers all CRA obligations for incorporated
contractors in British Columbia."
```

This approach is expensive (requires one LLM call per chunk) but can improve retrieval accuracy by 20-35% on ambiguous queries.

---

## 5. Hybrid Chunking: The Production Pattern

The most effective production systems combine multiple strategies:

### Recommended Hybrid Pipeline

```
Document Input
    |
    v
[1. Markdown Header Splitter]  -- Split on H1/H2/H3
    |
    v
[2. Size Check]  -- Is section > 512 tokens?
    |           |
    No          Yes
    |           |
    v           v
[Keep as-is]  [3. Recursive Splitter with 50-token overlap]
    |           |
    v           v
[4. Metadata Enrichment]  -- Prepend header path + doc title
    |
    v
[5. Embed and Store]  -- Generate vector, store in sqlite-vec
```

### Parent-Child Retrieval (Small-to-Big)

For complex documents requiring both precision and context, implement a two-tier index:

- **Child chunks** (256 tokens): Used for vector similarity search -- high precision matching
- **Parent chunks** (1024+ tokens): The full section containing the child -- fed to the LLM for generation

This decouples "what to search for" from "what to give the LLM," solving the fundamental tension in chunk sizing.

---

## 6. Advanced Strategies: Late Chunking and Proposition-Based

### Late Chunking (Jina AI, 2025)

Process the entire document through the embedding model first, then apply chunk boundaries to the token-level embeddings. Each chunk retains awareness of the full document context because the model saw everything before the chunking step.

- **Advantage:** No need for LLM-based context enrichment
- **Requirement:** Embedding model with long context window (8K+ tokens)
- **Best for:** Dense technical documents where cross-reference context matters

### Proposition-Based Chunking

Use an LLM to decompose text into atomic, self-contained factual statements. Each proposition becomes one chunk.

- **Advantage:** Maximum retrieval precision -- each chunk = one fact
- **Disadvantage:** Expensive (LLM call per document), high chunk count
- **Best for:** Knowledge bases where precise fact retrieval is critical

### Agentic Chunking

An LLM agent analyzes document structure and makes dynamic splitting decisions based on content density, topic shifts, and semantic importance.

- **Advantage:** Adapts to document complexity automatically
- **Disadvantage:** Slowest and most expensive approach
- **Best for:** Heterogeneous document collections with varying structures

---

## 7. Evaluation Metrics for Chunk Quality

To objectively measure whether your chunking strategy is working:

### Retrieval Metrics

| Metric | What It Measures | Target |
|:-------|:-----------------|:-------|
| **Recall@k** | % of relevant chunks found in top k results | > 0.85 at k=5 |
| **MRR** | Average reciprocal rank of first relevant result | > 0.70 |
| **nDCG** | Ranking quality with graded relevance | > 0.75 |
| **Precision@k** | % of top k results that are relevant | > 0.60 at k=5 |

### Generation Quality Metrics

| Metric | What It Measures | Tool |
|:-------|:-----------------|:-----|
| **Faithfulness** | Is the answer supported by retrieved chunks? | RAGAS, LlamaIndex |
| **Relevancy** | Does the answer address the query? | RAGAS |
| **Contextual Recall** | Do retrieved chunks contain all needed info? | LLM-as-judge |

### Practical Evaluation Approach

1. Create a test set of 20-30 representative queries with known-correct source chunks
2. Run retrieval with different chunk configurations
3. Measure Recall@5 and MRR for each configuration
4. Select the configuration with highest Recall@5 (prioritize finding the right info)

---

## 8. sqlite-vec Performance Considerations

Our Keystone brain uses sqlite-vec for vector storage. Key performance characteristics:

### Scale vs. Latency (Brute-Force Search)

| Vector Count | Expected Latency | Notes |
|:-------------|:-----------------|:------|
| 1,000-10,000 | < 20ms | Excellent -- our current scale |
| 10,000-100,000 | 50-100ms | Still fast, comfortable range |
| 100,000-500,000 | 100-500ms | Consider quantization |
| 1,000,000+ | > 1 second | Brute-force becomes limiting |

### Impact of Chunk Size on sqlite-vec

- **More chunks = more vectors = slower brute-force search** (linear scaling)
- **Smaller chunks increase total vector count** but each vector is more focused
- At our current scale (~1,158 chunks), sqlite-vec performs exceptionally well regardless of chunk size
- Even doubling to 2,500 chunks with smaller sizing would remain sub-50ms

### Optimization Strategies

1. **Int8 Quantization:** Reduces vector storage by 4x with minimal accuracy loss
2. **Dimension Reduction:** If using 1536d embeddings, truncating to 768d or 384d speeds up distance calculations
3. **mmap_size tuning:** Increasing SQLite mmap_size improves read performance for vector scans
4. **Metadata pre-filtering:** Use WHERE clauses on metadata columns before vector search to reduce scan scope

### Recommendation for Keystone Brain

At our current scale of ~1,200 chunks, performance is not a concern. We can safely increase chunk count by 3-5x without noticeable latency impact. Focus optimization efforts on chunk quality (content and metadata) rather than index tuning.

---

## 9. Specific Recommendations for Keystone Brain

Based on all research findings, here is the recommended configuration:

### Immediate Implementation

```
Chunk Size:          512 tokens (approx 2,000 characters)
Overlap:             50 tokens (10%) -- only for recursive sub-splitting
Primary Splitter:    MarkdownHeaderTextSplitter (H1/H2/H3)
Secondary Splitter:  RecursiveCharacterTextSplitter (fallback)
Metadata:            doc_title + header_path prepended to content
Min Chunk Size:      100 tokens (merge small sections up)
Max Chunk Size:      800 tokens (allow larger coherent sections)
```

### Metadata Schema

```python
chunk_metadata = {
    "doc_title": "Source document title",
    "header_path": "H1 > H2 > H3 hierarchy",
    "domain": "tax | legal | tech | content | wellness",
    "source_file": "filename.md",
    "chunk_index": 0,  # Position in document
    "ingestion_date": "2026-05-22",
}
```

### Priority Actions

1. **Implement heading-aware splitting** for all new document ingestion
2. **Prepend header context** to chunk content before embedding
3. **Set minimum chunk size** of 100 tokens to avoid micro-fragments
4. **Add domain metadata** to enable filtered retrieval
5. **Create a 20-query test set** for evaluating chunk quality changes
6. **Benchmark before/after** using Recall@5 and MRR metrics

---

## 10. Framework Comparison: LangChain vs LlamaIndex (2026)

| Feature | LangChain | LlamaIndex |
|:--------|:----------|:-----------|
| **Markdown splitting** | MarkdownHeaderTextSplitter | MarkdownNodeParser |
| **Recursive splitting** | RecursiveCharacterTextSplitter | SentenceSplitter |
| **Semantic chunking** | SemanticChunker (experimental) | SemanticSplitterNodeParser |
| **Parent-child** | ParentDocumentRetriever | NodeRelationships (built-in) |
| **Best for** | Agentic orchestration | RAG pipeline optimization |

### The Power Combo Pattern (2026 Best Practice)

Use LlamaIndex for data ingestion, chunking, and retrieval quality. Use LangChain (via LangGraph) for agentic orchestration of how retrieved chunks are consumed. Many production systems in 2026 use both frameworks together.

---

## Sources Consulted

- Industry benchmark reports on RAG chunking (NVIDIA, Databricks, 2024-2025)
- LangChain text splitter documentation and best practices
- LlamaIndex node parser and evaluation documentation
- sqlite-vec performance benchmarks (Alex Garcia, alexgarcia.xyz)
- Anthropic Contextual Retrieval technical blog
- Jina AI Late Chunking research paper
- RAGAS evaluation framework documentation
- Multiple practitioner reports on Medium, Towards Data Science, and arXiv
- Reddit and Hacker News community discussions on chunking optimization
- Unstructured.io and Docling documentation for structure-aware parsing


---
📁 **See also:** ← Directory Index
