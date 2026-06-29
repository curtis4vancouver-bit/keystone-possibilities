import urllib.request
import urllib.parse
import json
import os
import re
import time

def get_api_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ.get("GEMINI_API_KEY")
    for path in [
        r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.env",
        r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\.env"
    ]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return None

def search_ddg(query):
    """
    Scrape DuckDuckGo HTML search for real-time snippets.
    """
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            results = []
            for s in snippets[:6]:
                clean = re.sub(r'<[^>]*>', '', s).strip()
                # Unescape some common HTML entities
                clean = clean.replace("&quot;", '"').replace("&#x27;", "'").replace("&amp;", "&")
                results.append(clean)
            return results
    except Exception as e:
        print(f"[DebateEngine] DDG Search error: {e}")
        return []

def call_gemini(prompt, system_instruction=None, json_mode=False):
    """
    Call Gemini 2.5 Flash API using raw HTTP requests.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable or .env config not found.")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    if system_instruction:
        body["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }
        
    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"
        
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = response.read().decode('utf-8')
            res_json = json.loads(res_data)
            return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"[DebateEngine] Gemini API error: {e}")
        raise

def run_quant_debate(market):
    """
    Runs the full Bull/Bear/Execution/Risk debate loop for a single market dictionary.
    """
    question = market["question"]
    yes_price = market["outcomePrices"][0]
    no_price = market["outcomePrices"][1]
    
    print(f"\n[DebateEngine] Starting debate for: '{question}'")
    print(f"[DebateEngine] Current Market Prices: YES: ${yes_price:.2f} | NO: ${no_price:.2f}")
    
    # 1. Fetch search context
    print("[DebateEngine] Gathering latest search context...")
    snippets = search_ddg(question)
    context = "\n".join([f"- {s}" for s in snippets]) if snippets else "No search results available."
    print(f"[DebateEngine] Retrieved {len(snippets)} context snippets.")
    
    # 2. Bull Analyst
    print("[DebateEngine] Running Bull Analyst simulation...")
    bull_sys = (
        "You are the Bull Analyst. Your objective is to build the strongest possible logical case FOR "
        "the 'YES' outcome of the question. Base your arguments on search facts, trend analysis, and "
        "positive market sentiment. Do not admit downside risk or express doubts. Focus solely on YES arguments."
    )
    bull_prompt = f"Question: {question}\n\nSearch Context:\n{context}\n\nBuild the best case for YES."
    bull_argument = call_gemini(bull_prompt, system_instruction=bull_sys)
    
    # 3. Bear Analyst
    print("[DebateEngine] Running Bear Analyst simulation...")
    bear_sys = (
        "You are the Bear Analyst. Your objective is to build the strongest possible logical case FOR "
        "the 'NO' outcome of the question. Base your arguments on search facts, risks, obstacles, and "
        "negative market sentiment. Do not admit upside potential. Focus solely on NO arguments."
    )
    bear_prompt = f"Question: {question}\n\nSearch Context:\n{context}\n\nBuild the best case for NO."
    bear_argument = call_gemini(bear_prompt, system_instruction=bear_sys)
    
    # 4. Execution Agent
    print("[DebateEngine] Running Execution Agent arbitration...")
    execution_sys = (
        "You are the Execution Agent. Your task is to weigh the arguments presented by the Bull and Bear Analysts "
        "objectively. You must assess the probability p (float between 0.0 and 1.0) of the 'YES' outcome based on "
        "the strength of evidence. Then output a JSON response containing 'probability' (float), 'reasoning' (text), "
        "and 'recommended_outcome' ('YES', 'NO', or 'NONE')."
    )
    execution_prompt = (
        f"Question: {question}\n\n"
        f"Current Prices: YES = ${yes_price:.2f}, NO = ${no_price:.2f}\n\n"
        f"--- BULL ARGUMENT ---\n{bull_argument}\n\n"
        f"--- BEAR ARGUMENT ---\n{bear_argument}\n\n"
        f"Arbitrate the arguments and recommend the best outcome in JSON format."
    )
    
    execution_raw = call_gemini(execution_prompt, system_instruction=execution_sys, json_mode=True)
    execution_result = json.loads(execution_raw)
    
    prob = float(execution_result.get("probability", 0.5))
    reasoning = execution_result.get("reasoning", "")
    decision = execution_result.get("recommended_outcome", "NONE").upper()
    
    print(f"[DebateEngine] Execution Decision: {decision} | Evaluated Prob: {prob*100:.1f}%")
    
    # 5. Risk Manager (Kelly Criterion Sizing)
    # f = (p * b - q) / b = (p - C) / (1 - C)
    # We apply a Half-Kelly fraction (0.5 multiplier) for portfolio safety.
    wager_amount = 0.0
    kelly_fraction = 0.0
    edge = 0.0
    
    from portfolio_manager import load_portfolio
    portfolio = load_portfolio()
    cash = portfolio["cash"]
    
    trade_outcome = None
    trade_price = 0.0
    
    if decision == "YES":
        edge = prob - yes_price
        trade_price = yes_price
        trade_outcome = "YES"
        if edge > 0:
            kelly_fraction = edge / (1 - yes_price)
    elif decision == "NO":
        prob_no = 1.0 - prob
        edge = prob_no - no_price
        trade_price = no_price
        trade_outcome = "NO"
        if edge > 0:
            kelly_fraction = edge / (1 - no_price)
            
    if kelly_fraction > 0:
        # Limit max wager to 20% of cash for safety, even if Kelly suggests more
        safe_fraction = min(kelly_fraction * 0.5, 0.20)
        wager_amount = cash * safe_fraction
        
    return {
        "question": question,
        "market_id": market["id"],
        "yes_price": yes_price,
        "no_price": no_price,
        "context": context,
        "bull_argument": bull_argument,
        "bear_argument": bear_argument,
        "probability": prob,
        "reasoning": reasoning,
        "decision": decision,
        "edge": edge,
        "kelly_fraction": kelly_fraction,
        "wager_amount": wager_amount,
        "trade_outcome": trade_outcome,
        "trade_price": trade_price
    }
