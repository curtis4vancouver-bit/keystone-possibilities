# Vector Similarity Search Threshold Tuning to Eliminate Hallucination Matches

**Research Date:** May 22, 2026
**Domain:** vector_brain_optimization
**Researcher:** Keystone Overnight Research Agent

---

## Executive Summary

Vector similarity search thresholds are the primary gatekeeper between your knowledge base and your LLM. Setting them incorrectly is the single largest contributor to two failure modes: (1) **hallucination via noise injection** (threshold too low, irrelevant chunks pollute the context), and (2) **hallucination via context starvation** (threshold too high, the LLM lacks evidence and falls back on pretrained weights). This report provides actionable guidance for calibrating thresholds, implementing reranking, and building multi-stage retrieval pipelines -- with specific attention to sqlite-vec deployments.

---

## 1. Cosine Similarity Score Thresholds for RAG

There is **no universal optimal cosine similarity threshold**. Scores depend on the embedding model, domain data, and query type. However, practitioners converge on these heuristic ranges as starting points:

| Threshold Range | Interpretation | Typical Use Case |
|:---|:---|:---|
| **0.90+** | Near-perfect match | Deduplication, exact-match verification |
| **0.70 - 0.85** | Highly relevant | General-purpose RAG (balanced precision/recall) |
| **0.50 - 0.65** | Moderately relevant | Exploratory queries, broad topic coverage |
| **0.30 - 0.45** | Weak connection | Usually noise; high hallucination risk |

**Critical insight:** These ranges assume older models like `text-embedding-ada-002`. Newer models produce fundamentally different score distributions (see Section 2).

---

## 2. Calibrating Thresholds Across Embedding Models

Different embedding models inhabit different vector spaces. A score of 0.80 in one model is NOT equivalent to 0.80 in another.

### Observed Score Distributions by Model

| Model | Typical High-Quality Match Score | Notes |
|:---|:---|:---|
| `text-embedding-ada-002` | 0.80 - 0.90 | Historical OpenAI model; clusters high |
| `text-embedding-3-small/large` | 0.30 - 0.50 | Newer OpenAI; dramatically lower absolute scores |
| `all-MiniLM-L6-v2` | 0.60 - 0.80 | Popular open-source; moderate range |
| Cohere `embed-v3` | 0.40 - 0.65 | Varies by language and domain |

### Calibration Process

1. **Generate a Representative Sample:** Embed 200-500 documents from your actual corpus using the target model.
2. **Compute Pairwise Scores:** Calculate cosine similarity for known-relevant pairs, known-irrelevant pairs, and random pairs.
3. **Plot the Distribution:** Create a histogram of scores. Look for natural gaps between relevant and irrelevant clusters -- that gap is your threshold zone.
4. **Use Precision-Recall Curves:** With labeled validation data, plot PR curves and select the threshold that maximizes your priority metric (F1, precision, or recall depending on use case).
5. **Near-Miss Analysis:** Manually review pairs just above and below your candidate threshold. If irrelevant content appears above the line, raise it. If good content falls below, lower it.

### Practical Code Example for Calibration

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def analyze_threshold(embeddings_relevant, embeddings_irrelevant, query_embedding):
    """Analyze score distributions to find optimal threshold."""
    relevant_scores = cosine_similarity([query_embedding], embeddings_relevant)[0]
    irrelevant_scores = cosine_similarity([query_embedding], embeddings_irrelevant)[0]
    
    print(f"Relevant scores - min: {relevant_scores.min():.3f}, "
          f"mean: {relevant_scores.mean():.3f}, max: {relevant_scores.max():.3f}")
    print(f"Irrelevant scores - min: {irrelevant_scores.min():.3f}, "
          f"mean: {irrelevant_scores.mean():.3f}, max: {irrelevant_scores.max():.3f}")
    
    # Suggested threshold: midpoint between distributions
    suggested = (relevant_scores.min() + irrelevant_scores.max()) / 2
    print(f"Suggested threshold: {suggested:.3f}")
    return suggested
```

---

## 3. False Positive Elimination in Vector Search

False positives -- results that are semantically "close" but factually irrelevant -- are the primary source of hallucination-inducing noise. Strategies to eliminate them:

### Multi-Layer Defense

1. **Metadata Pre-Filtering:** Apply hard constraints (date ranges, document categories, tenant IDs) BEFORE vector search to exclude entire irrelevant document subsets.
2. **Cross-Encoder Reranking:** After initial retrieval, use a cross-encoder to re-score query-document pairs with token-level attention (see Section 4).
3. **Hybrid Search:** Combine vector search with BM25 keyword matching to catch exact-term failures (see Section 8).
4. **Negative Feedback Loops:** Track consistently false-positive documents and add them to exclusion lists or use them to fine-tune embeddings.
5. **Score Distribution Monitoring:** Alert when the distribution of returned scores shifts significantly -- this indicates data drift or model degradation.

---

## 4. Cross-Encoder Reranking Strategies

Cross-encoder reranking is the single most effective technique for improving precision after initial vector retrieval. Unlike bi-encoders (which encode query and document independently), cross-encoders process query+document together, enabling fine-grained semantic understanding.

### Two-Stage Architecture

```
Stage 1: Bi-Encoder (fast)          Stage 2: Cross-Encoder (precise)
Query --> Embed --> Top-100 ANN --> Rerank with cross-encoder --> Top-5 to LLM
```

### How It Works

1. **Stage 1 (Retrieval):** Use bi-encoder/vector search to retrieve top 50-200 candidates. Optimized for recall.
2. **Stage 2 (Reranking):** Pass all candidates through a cross-encoder model that computes fine-grained relevance scores. Optimized for precision.
3. **Final Selection:** Keep only the top 3-5 results based on reranker scores.

### Recommended Cross-Encoder Models

| Model | Size | Speed | Quality |
|:---|:---|:---|:---|
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | 23M params | Fast | Good baseline |
| `cross-encoder/ms-marco-MiniLM-L-12-v2` | 33M params | Medium | Better quality |
| `BAAI/bge-reranker-v2-m3` | 568M params | Slower | [[STATE|State]]-of-the-art |
| Cohere Rerank API | Managed | Fast | Production-grade |

### Key Insight for Thresholding

**Use reranker scores for thresholding, not raw embedding scores.** Raw cosine similarity scores tend to cluster in narrow bands and are poorly calibrated for cutoff decisions. Cross-encoder scores are more interpretable and spread across a wider range, making them far better candidates for "is this relevant enough?" decisions.

---

## 5. MMR (Maximal Marginal Relevance) for Result Diversity

MMR balances relevance and diversity by iteratively selecting results that are similar to the query but dissimilar to already-selected results. This prevents redundant chunks from consuming context window budget.

### The MMR Formula

```
MMR = argmax [ lambda * Sim(doc, query) - (1 - lambda) * max(Sim(doc, selected)) ]
```

### Lambda Tuning Guide

| Lambda | Behavior | Use Case |
|:---|:---|:---|
| 1.0 | Pure relevance (standard search) | Factual lookups, narrow queries |
| 0.7 | Relevance-dominant with some diversity | Default for most RAG pipelines |
| 0.5 | Balanced | Exploratory queries, broad topics |
| 0.3 | Diversity-dominant | Information discovery, avoiding echo chambers |

### Implementation

Most vector stores support MMR natively:
- **Qdrant:** Built-in MMR parameter in search requests
- **LangChain:** `max_marginal_relevance_search()` method
- **OpenSearch:** Native MMR for k-NN queries

For custom implementations, the core loop fetches `fetch_k` candidates (e.g., 50), then iteratively selects `k` final results (e.g., 5) using the MMR scoring formula.

---

## 6. Top-K vs. Threshold-Based Cutoff Tradeoffs

| Dimension | Top-K | Threshold-Based |
|:---|:---|:---|
| **Result count** | Fixed, predictable | Variable (0 to many) |
| **Precision** | Degrades as K grows | High (rejects low-quality) |
| **Recall** | Controllable via K | Depends on data distribution |
| **Latency** | Consistent | Unpredictable |
| **Production safety** | Safe (bounded output) | Risk of 0 results or floods |

### The Hybrid Approach (Recommended)

```
1. Retrieve Top-K (K=50-100) for recall safety
2. Apply threshold filter to remove low-quality results
3. Rerank surviving candidates with cross-encoder
4. Pass top 3-5 to LLM
```

This gives you the production stability of Top-K with the quality guarantee of threshold filtering. If after threshold filtering you have zero results, trigger a "no answer" response rather than hallucinating.

---

## 7. Evaluating Retrieval Quality

### Core Metrics

| Metric | What It Measures | Best For |
|:---|:---|:---|
| **Precision@K** | Fraction of top-K results that are relevant | Measuring noise levels |
| **Recall@K** | Fraction of all relevant docs found in top-K | Measuring coverage |
| **MRR** | Reciprocal rank of first relevant result | Single-answer QA tasks |
| **NDCG@K** | Ranking quality with graded relevance | Multi-level relevance scenarios |
| **MAP** | Average precision across all relevant docs | Overall ranking quality |

### RAGAS Framework for Automated Evaluation

RAGAS (Retrieval Augmented Generation Assessment) is the industry standard for automated RAG evaluation. Key metrics:

- **Faithfulness:** Ratio of generated claims supported by context (hallucination detector). Score = supported_claims / total_claims.
- **Answer Relevancy:** How well the answer addresses the original query.
- **Context Precision:** Whether relevant chunks are ranked highly in retrieval.
- **Context Recall:** Whether all necessary information was retrieved.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

# Structure: question, answer, contexts, ground_truth
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
print(result)
```

### Human-in-the-Loop Validation

For critical systems, supplement automated metrics with human relevance judgments:
1. Sample 50-100 query-result pairs from production.
2. Have evaluators rate each result on a 1-5 relevance scale.
3. Compute NDCG against these graded judgments.
4. Track trends weekly to catch quality regressions.

---

## 8. Hybrid Search: Vector + BM25 for Higher Precision

Pure vector search fails on exact matches (product codes, error IDs, section numbers). Pure keyword search fails on semantic understanding. Combining them covers both blind spots.

### Fusion Methods

#### Reciprocal Rank Fusion (RRF) -- Industry Standard

```python
def reciprocal_rank_fusion(ranked_lists, k=60):
    """Combine multiple ranked lists using RRF."""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Usage: combine BM25 results and vector results
final_ranking = reciprocal_rank_fusion([bm25_results, vector_results])
```

#### Weighted Score Fusion

```
Final_Score = alpha * normalize(BM25_score) + (1 - alpha) * normalize(vector_score)
```

Typical alpha values: 0.3-0.5 for general use; higher alpha for keyword-heavy domains.

### Production Pipeline

```
Query --> [BM25 Index] --> Top-100 keyword results  \
      --> [Vector DB]  --> Top-100 vector results    --> RRF Fusion --> Rerank --> Top-5 --> LLM
```

---

## 9. sqlite-vec Specific Threshold Tuning

sqlite-vec uses brute-force SIMD-accelerated scans via `vec0` virtual tables. Key configuration and tuning details:

### Distance Metric Configuration

```sql
-- Create table with cosine distance (recommended for LLM embeddings)
CREATE VIRTUAL TABLE vec_documents USING vec0(
    document_id INTEGER PRIMARY KEY,
    contents_embedding FLOAT[1536] distance_metric=cosine
);
```

### KNN Query with Distance Threshold

```sql
-- Standard KNN (Top-K approach)
SELECT document_id, distance 
FROM vec_documents 
WHERE contents_embedding MATCH vec_f32(?)
AND k = 20;

-- KNN with distance threshold (hybrid approach)
SELECT document_id, distance 
FROM vec_documents 
WHERE contents_embedding MATCH vec_f32(?)
AND k = 50
AND distance < 0.4;  -- cosine distance threshold
```

### Distance Metric Ranges

| Metric | Range | "Similar" Values | "Dissimilar" Values |
|:---|:---|:---|:---|
| Cosine Distance | 0.0 - 2.0 | Near 0.0 | Near 2.0 |
| Cosine Similarity | -1.0 - 1.0 | Near 1.0 | Near -1.0 |
| L2 (Euclidean) | 0.0 - infinity | Near 0.0 | Large values |

**Important:** sqlite-vec returns cosine DISTANCE (not similarity). To convert: `similarity = 1.0 - distance`. A distance of 0.3 equals similarity of 0.7.

### Manual Distance Computation (for threshold filtering outside vec0)

```sql
SELECT 
    id, 
    vec_distance_cosine(embedding, vec_f32(?)) AS distance
FROM documents_table
WHERE distance < 0.5
ORDER BY distance ASC
LIMIT 10;
```

### Normalization

If using cosine distance, ensure vectors are normalized:

```sql
-- Normalize a vector before insertion
INSERT INTO vec_documents(document_id, contents_embedding)
VALUES (1, vec_normalize(vec_f32(?)));
```

### Metadata Pre-Filtering (v0.1.6+)

```sql
CREATE VIRTUAL TABLE vec_articles USING vec0(
    article_id INTEGER PRIMARY KEY,
    headline_embedding FLOAT[384],
    category TEXT,
    year INTEGER partition key  -- partition key for fast filtering
);

-- Efficient metadata-filtered vector search
SELECT article_id, distance 
FROM vec_articles 
WHERE headline_embedding MATCH vec_f32(?)
  AND k = 10
  AND year = 2026
  AND category = 'construction';
```

---

## 10. Impact of Threshold Settings on Hallucination Rates

The relationship between retrieval quality and hallucination is direct and measurable:

### The Two Failure Modes

| Failure Mode | Cause | Symptom |
|:---|:---|:---|
| **Noise Injection** | Threshold too low; irrelevant chunks enter context | LLM confabulates by "stitching together" unrelated facts |
| **Context Starvation** | Threshold too high; relevant chunks excluded | LLM falls back on pretrained weights, producing outdated/wrong answers |

### Mitigation Checklist

1. **Threshold on reranker scores, not raw embeddings.** Reranker scores are calibrated and interpretable.
2. **Implement "I don't know" grounding.** If top retrieved chunks score below threshold, return a no-answer rather than hallucinating.
3. **Force citations in generation.** Require the LLM to cite specific source IDs for every claim. This makes unsupported claims immediately visible.
4. **Use contextual compression.** Extract only the most relevant sentences from retrieved chunks before passing to the LLM. This reduces the "lost in the middle" problem.
5. **Self-verification loop.** After generation, run a lightweight LLM pass to check if the answer is fully supported by the retrieved context. Flag unsupported claims.
6. **Continuous monitoring with RAGAS.** Track Faithfulness scores in production. A drop indicates either retrieval degradation or threshold misconfiguration.

### System Prompt Template for Grounded Generation

```
You are an expert assistant. Answer ONLY using the provided context below.
If the context does not contain the answer, say: "I do not have enough 
information to answer this question."
Do NOT use any outside knowledge. Cite the source [ID] for each claim.

Context:
{retrieved_chunks}
```

---

## Summary: Recommended Production Configuration

| Component | Recommendation |
|:---|:---|
| **Distance Metric** | Cosine distance (matches most embedding models) |
| **Initial Retrieval** | Top-50 candidates via hybrid search (vector + BM25 with RRF) |
| **Reranking** | Cross-encoder on top-50, keep top-5 |
| **Threshold** | Apply on reranker scores (calibrate per model/domain) |
| **Diversity** | MMR with lambda=0.7 if redundancy is observed |
| **No-Answer Policy** | If max reranker score < threshold, return "insufficient data" |
| **Evaluation** | RAGAS Faithfulness + Context Precision weekly |
| **sqlite-vec** | `distance_metric=cosine`, partition keys for metadata, `vec_normalize()` |

---

## Sources Consulted

- OpenAI Community Forums - Embedding threshold discussions
- Pinecone Documentation - Retrieval evaluation metrics
- Weaviate Documentation - Hybrid search and reranking
- Qdrant Documentation - MMR implementation
- sqlite-vec Documentation - vec0 virtual table configuration
- RAGAS Framework Documentation - Faithfulness scoring
- Redis Vector Search Documentation - Hybrid search architecture
- Milvus Documentation - Distance metrics and filtering
- Elastic Documentation - MMR and BM25 integration
- Various research papers on RAG hallucination mitigation (arXiv)
- Stack Exchange and Reddit practitioner discussions
- Towards Data Science, Medium technical articles


---
📁 **See also:** ← Directory Index
