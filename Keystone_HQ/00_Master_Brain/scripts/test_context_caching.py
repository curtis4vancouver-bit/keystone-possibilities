import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load local environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def test_caching():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[Error] No GEMINI_API_KEY or GOOGLE_API_KEY found.")
        return

    print("[Cache Test] Initializing Gemini Client...")
    client = genai.Client(api_key=api_key)
    
    # Context caching has a minimum token count requirement (typically 32,768 tokens)
    # We will generate a large data block of repeated context to exceed the minimum threshold.
    print("[Cache Test] Building large context block...")
    base_text = "The Keystone possibilities brand is a high-end PM and construction company located in Squamish. "
    large_context = base_text * 4500  # Creates ~36,000 words (exceeds 32,768 token threshold)
    
    model_id = "gemini-3.5-flash"
    
    print("[Cache Test] Creating Context Cache on Google servers (expires in 10 minutes)...")
    try:
        cache = client.caches.create(
            model=model_id,
            config=types.CreateCachedContentConfig(
                display_name="keystone_knowledge_base_cache",
                system_instruction="You are an expert assistant for Keystone Possibilities.",
                contents=[large_context],
                ttl="600s", # 10 minutes
            )
        )
        print(f"[Cache Test] Cache created successfully! Name: {cache.name}")
        
        # Test Query using the Cache
        print("[Cache Test] Running query using the cache reference...")
        response = client.models.generate_content(
            model=model_id,
            contents="Based on the context, where is the Keystone possibilities brand located?",
            config=types.GenerateContentConfig(
                cached_content=cache.name
            )
        )
        
        print("=" * 60)
        print("QUERY SUCCESS WITH CACHED CONTENT!")
        print("=" * 60)
        print("Response text:", response.text)
        print("=" * 60)
        
        # Cleanup
        print("[Cache Test] Cleaning up and deleting cache...")
        client.caches.delete(name=cache.name)
        print("[Cache Test] Cache deleted successfully.")
        
    except Exception as e:
        print(f"[Error] Caching execution failed: {e}")

if __name__ == "__main__":
    test_caching()
