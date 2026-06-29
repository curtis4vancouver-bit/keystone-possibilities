"""
Keystone Cost-Aware Context Router and Caching Middleware
=========================================================
Implements the crossover point mathematical models defined in Master_Docs/23_LLM_COST_AND_ROUTING_ARCHITECTURE.md.
Dynamically routes queries to the most cost-effective model (Gemini 3.5 Pro Cached vs. Gemini 3.5 Flash PayGo)
and manages Google GenAI SDK context caches.
"""

import os
import sys
import json
import time
from typing import Dict, Any, Tuple, Optional

# Force UTF-8 stdout
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Model Pricing Model (Pricing per 1M tokens)
PRICING = {
    "flash": {
        "input": 1.50,        # $1.50 per 1M tokens
        "output": 9.00,       # $9.00 per 1M tokens (includes reasoning/thinking tokens)
        "storage": 1.00,      # $1.00 per 1M tokens/hour
    },
    "pro": {
        "input": 2.50,        # $2.50 per 1M tokens
        "input_cached": 0.25, # $0.25 per 1M tokens (90% discount)
        "output": 15.00,      # $15.00 per 1M tokens
        "storage": 4.50,      # $4.50 per 1M tokens/hour
    }
}

class CostAwareContextRouter:
    def __init__(self, client: Optional[Any] = None):
        """
        Initialize the router with an optional genai.Client instance.
        """
        self.client = client
        self._load_sdk()

    def _load_sdk(self):
        if self.client is None:
            try:
                from google import genai
                self.client = genai.Client()
            except Exception:
                self.client = None

    def estimate_tokens(self, text: str) -> int:
        """Estimates token count. Uses exact count if SDK is active, else char approximation (4 chars/token)."""
        if self.client and hasattr(self.client, "models"):
            try:
                # Use a fast lightweight model to count tokens
                resp = self.client.models.count_tokens(
                    model="gemini-2.5-flash",
                    contents=text
                )
                return resp.total_tokens
            except Exception:
                pass
        return len(text) // 4

    def calculate_crossover(
        self,
        context_tokens: int,
        query_tokens: int,
        runs: int = 5,
        hours: float = 3.0,
        complexity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Calculates the crossover math ($N^*$) to determine if Gemini Pro with Cache is cheaper than Flash.
        
        Parameters:
        - context_tokens: Size of static codebase/context (C)
        - query_tokens: Size of dynamic instructions (Q)
        - runs: Expected executions (N)
        - hours: Cache storage lifetime (H)
        - complexity: Complexity rating ("low", "medium", "high") to estimate failure multiplier (K)
        """
        # Convert to millions of tokens for pricing formulas
        C = context_tokens / 1_000_000.0
        Q = query_tokens / 1_000_000.0
        H = hours
        
        # Estimate failure multipliers (K_F: Flash failure turns, K_P: Pro failure turns)
        if complexity == "high":
            K_F = 3.5  # Flash needs 3-4 attempts on very complex code
            K_P = 1.0  # Pro succeeds in 1
            T_F = 0.002 # 2k thinking tokens
            T_P = 0.008 # 8k thinking tokens
        elif complexity == "medium":
            K_F = 2.0  # Flash needs 2 attempts
            K_P = 1.0  # Pro succeeds in 1
            T_F = 0.001
            T_P = 0.004
        else: # low
            K_F = 1.2  # Flash usually gets it first time
            K_P = 1.0
            T_F = 0.0
            T_P = 0.0
            
        # Expected outputs size (visible tokens)
        R_F = 0.002 # 2k tokens
        R_P = 0.002 # 2k tokens

        # Formulas from Master_Docs/23_LLM_COST_AND_ROUTING_ARCHITECTURE.md
        # Cost of Flash Uncached
        flash_cost_per_run = ((C + Q) * PRICING["flash"]["input"]) + ((T_F + R_F) * PRICING["flash"]["output"])
        total_flash_cost = runs * K_F * flash_cost_per_run

        # Cost of Pro Cached (Fixed write cost + storage + marginal runs)
        pro_fixed_cost = (C * PRICING["pro"]["input"]) + (C * H * PRICING["pro"]["storage"])
        pro_marginal_cost_per_run = (
            (C * PRICING["pro"]["input_cached"]) + 
            (Q * PRICING["pro"]["input"]) + 
            ((T_P + R_P) * PRICING["pro"]["output"])
        )
        total_pro_cached_cost = pro_fixed_cost + (runs * K_P * pro_marginal_cost_per_run)

        # Crossover Threshold N*
        # N* = FC_P / (MC_F - MC_P)
        mc_flash = K_F * flash_cost_per_run
        mc_pro_cached = K_P * pro_marginal_cost_per_run
        
        if mc_flash > mc_pro_cached:
            n_star = pro_fixed_cost / (mc_flash - mc_pro_cached)
        else:
            n_star = float('inf')

        # Recommendation Engine
        should_cache = context_tokens >= 32768 and runs > n_star and n_star != float('inf')
        
        if should_cache:
            recommended_model = "gemini-2.5-pro"
            route_mode = "cached_pro"
        elif context_tokens >= 32768:
            # Context is large, but runs are few -> Pro uncached or Flash uncached
            if total_flash_cost < (C * PRICING["pro"]["input"] + pro_marginal_cost_per_run * runs):
                recommended_model = "gemini-2.5-flash"
                route_mode = "uncached_flash"
            else:
                recommended_model = "gemini-2.5-pro"
                route_mode = "uncached_pro"
        else:
            recommended_model = "gemini-2.5-flash"
            route_mode = "uncached_flash"

        return {
            "context_tokens": context_tokens,
            "query_tokens": query_tokens,
            "complexity": complexity,
            "estimated_runs": runs,
            "cache_lifetime_hours": hours,
            "n_star_threshold": round(n_star, 2) if n_star != float('inf') else "N/A",
            "flash_uncached_total_cost": round(total_flash_cost, 4),
            "pro_cached_total_cost": round(total_pro_cached_cost, 4),
            "savings": round(total_flash_cost - total_pro_cached_cost, 4),
            "should_cache": should_cache,
            "recommended_model": recommended_model,
            "route_mode": route_mode,
            "parameters": {
                "max_output_tokens": 8192 if recommended_model == "gemini-2.5-pro" else 2048,
                "thinking_budget": 4096 if recommended_model == "gemini-2.5-pro" else 0
            }
        }

    def create_context_cache(self, model: str, static_content: str, ttl_seconds: int = 10800) -> Optional[str]:
        """
        Creates a context cache in Google GenAI SDK if client is active.
        Returns the cache name/ID.
        """
        if not self.client:
            print("[Cost Router] Warning: SDK Client not active. Caching skipped.")
            return None

        try:
            print(f"[Cost Router] Registering context cache on '{model}' (TTL: {ttl_seconds}s)...")
            cache = self.client.caches.create(
                model=model,
                config=types.CreateCachedContentConfig(
                    contents=[static_content],
                    ttl=f"{ttl_seconds}s",
                    display_name=f"keystone-context-{int(time.time())}"
                )
            )
            print(f"[Cost Router] Cache created successfully: {cache.name}")
            return cache.name
        except Exception as e:
            print(f"[Cost Router Error] Failed to create context cache: {e}")
            return None

    def route(
        self,
        static_content: str,
        dynamic_query: str,
        expected_runs: int = 5,
        complexity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Main gateway router. Determines cost-effectiveness, creates cache if needed,
        and returns configuration settings for execution.
        """
        c_tokens = self.estimate_tokens(static_content)
        q_tokens = self.estimate_tokens(dynamic_query)
        
        analysis = self.calculate_crossover(
            context_tokens=c_tokens,
            query_tokens=q_tokens,
            runs=expected_runs,
            hours=3.0,
            complexity=complexity
        )
        
        # Setup final execution payload
        route_payload = {
            "model": analysis["recommended_model"],
            "cache_name": None,
            "max_output_tokens": analysis["parameters"]["max_output_tokens"],
            "thinking_budget": analysis["parameters"]["thinking_budget"],
            "mode": analysis["route_mode"],
            "analysis": analysis
        }

        # Handle cache creation
        if analysis["should_cache"] and self.client:
            cache_id = self.create_context_cache(
                model=analysis["recommended_model"],
                static_content=static_content,
                ttl_seconds=10800
            )
            route_payload["cache_name"] = cache_id
            
        return route_payload

# Validation run
if __name__ == "__main__":
    router = CostAwareContextRouter()
    
    # Simulate a codebase sweep: 400,000 tokens of static codebase, 15,000 tokens query, 5 runs
    result = router.calculate_crossover(
        context_tokens=400_000,
        query_tokens=15_000,
        runs=5,
        hours=3.0,
        complexity="medium"
    )
    print("Codebase Sweep Simulation Results:")
    print(json.dumps(result, indent=2))
