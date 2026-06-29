import json
import os
import time

PORTFOLIO_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "simulated_portfolio.json"
)

DEFAULT_PORTFOLIO = {
    "cash": 10000.0,
    "positions": {},
    "history": []
}

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "cash": 10000.0,
        "positions": {},
        "history": []
    }

def save_portfolio(portfolio):
    try:
        with open(PORTFOLIO_FILE, "w") as f:
            json.dump(portfolio, f, indent=2)
    except Exception as e:
        print(f"[PortfolioManager] Error saving portfolio: {e}")

def buy_position(market_id, question, outcome, price, wager_amount):
    portfolio = load_portfolio()
    if portfolio["cash"] < wager_amount:
        print(f"[PortfolioManager] Insufficient cash to wager ${wager_amount:.2f}. Available: ${portfolio['cash']:.2f}")
        return False, "Insufficient cash"
        
    shares = wager_amount / price
    portfolio["cash"] -= wager_amount
    
    pos_key = f"{market_id}_{outcome}"
    if pos_key in portfolio["positions"]:
        existing = portfolio["positions"][pos_key]
        total_shares = existing["shares"] + shares
        total_cost = (existing["shares"] * existing["buy_price"]) + wager_amount
        existing["shares"] = total_shares
        existing["buy_price"] = total_cost / total_shares
    else:
        portfolio["positions"][pos_key] = {
            "market_id": market_id,
            "question": question,
            "outcome": outcome,
            "buy_price": price,
            "shares": shares,
            "wagered": wager_amount
        }
        
    portfolio["history"].append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "BUY",
        "market_id": market_id,
        "question": question,
        "outcome": outcome,
        "price": price,
        "shares": shares,
        "amount": wager_amount,
        "cash_after": portfolio["cash"]
    })
    
    save_portfolio(portfolio)
    print(f"[PortfolioManager] Simulated BUY successful: Bought {shares:.2f} shares of '{outcome}' on '{question}' at ${price:.2f} per share (Total: ${wager_amount:.2f})")
    return True, f"Bought {shares:.2f} shares"

def get_portfolio_summary(current_prices=None):
    """
    Returns a summary of the portfolio value.
    current_prices: dict mapping market_id to outcome prices list [yes_price, no_price]
    """
    portfolio = load_portfolio()
    total_val = portfolio["cash"]
    
    positions_summary = []
    for key, pos in portfolio["positions"].items():
        market_id = pos["market_id"]
        outcome = pos["outcome"]
        shares = pos["shares"]
        buy_price = pos["buy_price"]
        
        # Determine current price
        curr_price = buy_price
        if current_prices and market_id in current_prices:
            prices = current_prices[market_id]
            # outcomes: index 0 is Yes, index 1 is No
            curr_price = prices[0] if outcome.lower() == "yes" else prices[1]
            
        value = shares * curr_price
        total_val += value
        
        pnl = value - pos["wagered"]
        pnl_pct = (pnl / pos["wagered"]) * 100 if pos["wagered"] > 0 else 0.0
        
        positions_summary.append({
            "question": pos["question"],
            "outcome": outcome,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": curr_price,
            "value": value,
            "pnl": pnl,
            "pnl_pct": pnl_pct
        })
        
    total_pnl = total_val - 10000.0 # initial balance
    return {
        "cash": portfolio["cash"],
        "total_value": total_val,
        "total_pnl": total_pnl,
        "positions": positions_summary,
        "history": portfolio["history"]
    }
