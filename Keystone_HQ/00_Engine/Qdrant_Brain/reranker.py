import sys
import os
import logging

# Suppress HuggingFace progress bars and logging that corrupt MCP stdout protocol
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TQDM_DISABLE"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"

import warnings
warnings.filterwarnings("ignore")

# Kill ALL logging output to stdout — sentence_transformers and httpx use
# Python logging with handlers that write to stdout, corrupting MCP JSON-RPC.
logging.disable(logging.CRITICAL)

try:
    _real_stdout = sys.stdout
    sys.stdout = sys.stderr
    from sentence_transformers import CrossEncoder
    RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
    reranker_model = CrossEncoder(RERANKER_MODEL_NAME)
    sys.stdout = _real_stdout
    # Re-enable logging now that loading is done
    logging.disable(logging.NOTSET)
    print("Reranker loaded successfully.", file=sys.stderr)
except Exception as e:
    sys.stdout = _real_stdout if '_real_stdout' in dir() else sys.stdout
    logging.disable(logging.NOTSET)
    reranker_model = None
    print(f"Reranker not available: {e}", file=sys.stderr)

def rerank_results(query: str, candidates: list, top_k: int) -> list:
    if not reranker_model or not candidates:
        return candidates[:top_k]
    
    pairs = []
    for point in candidates:
        payload = getattr(point, 'payload', None) or getattr(point, 'metadata', None) or {}
        doc_text = payload.get('document', payload.get('text', ''))
        pairs.append([query, str(doc_text)[:512]])
        
    try:
        scores = reranker_model.predict(pairs)
        for i in range(len(candidates)):
            candidates[i].score = float(scores[i])
            
        candidates.sort(key=lambda x: getattr(x, 'score', 0), reverse=True)
    except Exception as e:
        print(f"Reranking failed: {e}")
        
    return candidates[:top_k]

