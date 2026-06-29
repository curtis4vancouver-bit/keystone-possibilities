import urllib.request
import urllib.parse
import json

BASE_URL = "https://gamma-api.polymarket.com"

def _parse_json_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            pass
    return []

def search_markets(query, limit=5):
    """
    Search for active, open markets on Polymarket matching a search query.
    """
    params = {
        "active": "true",
        "closed": "false",
        "limit": limit
    }
    if query:
        params["search"] = query
        
    url = f"{BASE_URL}/markets?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            for item in data:
                outcomes = _parse_json_list(item.get("outcomes"))
                # Ensure it's a binary option market with outcomes Yes/No
                if outcomes and len(outcomes) == 2:
                    prices_list = _parse_json_list(item.get("outcomePrices"))
                    prices = [0.5, 0.5]
                    if prices_list:
                        try:
                            prices = [float(p) for p in prices_list]
                        except Exception:
                            pass
                    
                    results.append({
                        "id": item.get("id"),
                        "question": item.get("question"),
                        "slug": item.get("slug"),
                        "description": item.get("description", ""),
                        "outcomes": outcomes,
                        "outcomePrices": prices,
                        "clobTokenIds": item.get("clobTokenIds", []),
                        "liquidity": float(item.get("liquidity", 0.0) or 0.0)
                    })
            # Sort by liquidity descending
            results.sort(key=lambda x: x["liquidity"], reverse=True)
            return results
    except Exception as e:
        print(f"[MarketClient] Error searching markets: {e}")
        return []

def get_market_details(slug):
    """
    Get detailed information for a single market by its slug.
    """
    url = f"{BASE_URL}/markets?slug={slug}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                item = data[0]
                outcomes = _parse_json_list(item.get("outcomes"))
                if not outcomes:
                    outcomes = ["Yes", "No"]
                prices_list = _parse_json_list(item.get("outcomePrices"))
                prices = [0.5, 0.5]
                if prices_list:
                    try:
                        prices = [float(p) for p in prices_list]
                    except Exception:
                        pass
                return {
                    "id": item.get("id"),
                    "question": item.get("question"),
                    "slug": item.get("slug"),
                    "description": item.get("description", ""),
                    "outcomes": outcomes,
                    "outcomePrices": prices,
                    "clobTokenIds": item.get("clobTokenIds", []),
                    "liquidity": float(item.get("liquidity", 0.0) or 0.0)
                }
            return None
    except Exception as e:
        print(f"[MarketClient] Error fetching market details for slug '{slug}': {e}")
        return None
