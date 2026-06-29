import argparse
import sys
import os

# Ensure package is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import market_client
import debate_engine
import portfolio_manager

def main():
    parser = argparse.ArgumentParser(description="TradingAgents Quant Debate Framework")
    parser.add_argument("--query", type=str, help="Search query to find Polymarket events")
    parser.add_argument("--slug", type=str, help="Specific Polymarket event slug")
    parser.add_argument("--initial-cash", type=float, help="Reset portfolio cash balance (optional)")
    
    args = parser.parse_args()
    
    # Optional reset of portfolio cash
    if args.initial_cash is not None:
        portfolio = portfolio_manager.load_portfolio()
        portfolio["cash"] = args.initial_cash
        portfolio["positions"] = {}
        portfolio_manager.save_portfolio(portfolio)
        print(f"[RunDebate] Portfolio cash reset to ${args.initial_cash:.2f}")
        
    market = None
    if args.slug:
        print(f"[RunDebate] Fetching market details for slug: {args.slug}")
        market = market_client.get_market_details(args.slug)
        if not market:
            print(f"[RunDebate] Error: Market with slug '{args.slug}' not found.")
            sys.exit(1)
    else:
        query = args.query or "GTA VI"
        print(f"[RunDebate] Searching active markets for query: '{query}'")
        markets = market_client.search_markets(query, limit=3)
        if not markets:
            print(f"[RunDebate] No active binary option markets found matching '{query}'.")
            sys.exit(0)
        # Select the one with highest liquidity
        market = markets[0]
        print(f"[RunDebate] Selected market with highest liquidity: '{market['question']}'")

    # Run debate
    result = debate_engine.run_quant_debate(market)
    
    # Print Debate Report
    print("\n" + "="*80)
    print("                      QUANT DEBATE FRAMEWORK REPORT")
    print("="*80)
    print(f"QUESTION:      {result['question']}")
    print(f"SLUG:          {market['slug']}")
    print(f"MARKET PRICES: YES = ${result['yes_price']:.2f} | NO = ${result['no_price']:.2f}")
    print("-"*80)
    
    print("\n[BULL ANALYST ARGUMENTS]")
    print(result["bull_argument"].strip())
    print("-"*80)
    
    print("\n[BEAR ANALYST ARGUMENTS]")
    print(result["bear_argument"].strip())
    print("-"*80)
    
    print("\n[EXECUTION AGENT DECISION]")
    print(f"Estimated YES Probability: {result['probability']*100:.1f}%")
    print(f"Recommended Side:          {result['decision']}")
    print(f"Reasoning:\n{result['reasoning'].strip()}")
    print("-"*80)
    
    print("\n[RISK MANAGER ANALYSIS]")
    print(f"Edge:             {result['edge']*100:.1f}%")
    print(f"Kelly Fraction:   {result['kelly_fraction']*100:.1f}%")
    print(f"Wager Amount:     ${result['wager_amount']:.2f}")
    
    if result["wager_amount"] > 0:
        print(f"Simulating trade: BUY {result['trade_outcome']} at ${result['trade_price']:.2f}")
        success, msg = portfolio_manager.buy_position(
            market_id=result["market_id"],
            question=result["question"],
            outcome=result["trade_outcome"],
            price=result["trade_price"],
            wager_amount=result["wager_amount"]
        )
    else:
        print("Decision: NO TRADE (Negative edge or recommended side is NONE).")
        
    print("-"*80)
    
    # Print current portfolio summary
    # map current market prices to outcome prices
    current_prices = {result["market_id"]: [result["yes_price"], result["no_price"]]}
    summary = portfolio_manager.get_portfolio_summary(current_prices)
    
    print("\n[SIMULATED PORTFOLIO STATUS]")
    print(f"Available Cash:      ${summary['cash']:.2f}")
    print(f"Total Portfolio Val: ${summary['total_value']:.2f}")
    print(f"Total Net PnL:       ${summary['total_pnl']:.2f}")
    
    if summary["positions"]:
        print("\nActive Open Positions:")
        for pos in summary["positions"]:
            print(f"- {pos['shares']:.2f} shares of '{pos['outcome']}' on '{pos['question']}'")
            print(f"  Bought at: ${pos['buy_price']:.2f} | Current: ${pos['current_price']:.2f} | Value: ${pos['value']:.2f} | PnL: ${pos['pnl']:.2f} ({pos['pnl_pct']:.1f}%)")
    else:
        print("\nNo active open positions.")
        
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
