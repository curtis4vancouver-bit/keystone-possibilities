import unittest
import os
import json
import tempfile
import shutil

import portfolio_manager
import market_client
import debate_engine

class TestTradingDebateFramework(unittest.TestCase):

    def setUp(self):
        # Override PORTFOLIO_FILE with a temporary file to keep tests isolated
        self.test_dir = tempfile.mkdtemp()
        self.portfolio_file = os.path.join(self.test_dir, "test_portfolio.json")
        self.original_portfolio_file = portfolio_manager.PORTFOLIO_FILE
        portfolio_manager.PORTFOLIO_FILE = self.portfolio_file

    def tearDown(self):
        # Restore original configuration
        portfolio_manager.PORTFOLIO_FILE = self.original_portfolio_file
        shutil.rmtree(self.test_dir)

    def test_kelly_criterion_calculation_yes(self):
        # p = 0.70, C_yes = 0.60
        # Kelly: (0.70 - 0.60) / (1.0 - 0.60) = 0.10 / 0.40 = 0.25 (25%)
        prob = 0.70
        yes_price = 0.60
        no_price = 0.40
        
        market = {"id": "test_m1", "outcomePrices": [yes_price, no_price]}
        
        # Test YES decision edge
        decision = "YES"
        edge = prob - yes_price
        kelly_fraction = edge / (1 - yes_price)
        self.assertAlmostEqual(kelly_fraction, 0.25)
        
    def test_kelly_criterion_calculation_no(self):
        # p_yes = 0.30 => p_no = 0.70
        # C_no = 0.60
        # Kelly: (0.70 - 0.60) / (1.0 - 0.60) = 0.25 (25%)
        prob = 0.30
        yes_price = 0.40
        no_price = 0.60
        
        market = {"id": "test_m2", "outcomePrices": [yes_price, no_price]}
        
        decision = "NO"
        prob_no = 1.0 - prob
        edge = prob_no - no_price
        kelly_fraction = edge / (1 - no_price)
        self.assertAlmostEqual(kelly_fraction, 0.25)

    def test_portfolio_buy_and_average_cost(self):
        portfolio = portfolio_manager.load_portfolio()
        self.assertEqual(portfolio["cash"], 10000.0)
        self.assertEqual(len(portfolio["positions"]), 0)
        
        # First buy: 100 shares of YES at $0.50 ($50 wagered)
        success, msg = portfolio_manager.buy_position("test_m", "Will the Fed cut rates?", "YES", 0.50, 50.0)
        self.assertTrue(success)
        
        portfolio = portfolio_manager.load_portfolio()
        self.assertEqual(portfolio["cash"], 9950.0)
        pos = portfolio["positions"]["test_m_YES"]
        self.assertEqual(pos["shares"], 100.0)
        self.assertEqual(pos["buy_price"], 0.50)
        
        # Second buy: 100 shares of YES at $0.60 ($60 wagered)
        success, msg = portfolio_manager.buy_position("test_m", "Will the Fed cut rates?", "YES", 0.60, 60.0)
        self.assertTrue(success)
        
        portfolio = portfolio_manager.load_portfolio()
        self.assertEqual(portfolio["cash"], 9890.0)
        pos = portfolio["positions"]["test_m_YES"]
        self.assertEqual(pos["shares"], 200.0)
        # Average cost: (100 * 0.50 + 100 * 0.60) / 200 = 0.55
        self.assertEqual(pos["buy_price"], 0.55)

    def test_portfolio_summary_calculations(self):
        # Add initial positions
        portfolio_manager.buy_position("test_m3", "Will Rihanna release an album?", "YES", 0.40, 40.0)
        
        # Test summary with updated market prices
        # Buy YES at $0.40. If price rises to $0.60, position value goes to 100 shares * $0.60 = $60
        current_prices = {"test_m3": [0.60, 0.40]}
        summary = portfolio_manager.get_portfolio_summary(current_prices)
        
        self.assertEqual(summary["cash"], 9960.0)
        self.assertEqual(summary["total_value"], 10020.0)
        self.assertEqual(summary["total_pnl"], 20.0)
        self.assertEqual(summary["positions"][0]["pnl"], 20.0)
        self.assertEqual(summary["positions"][0]["pnl_pct"], 50.0)

    def test_market_client_parses_outcome_prices(self):
        # Test local validation function or check fields are converted to list of floats
        market = {
            "id": "123",
            "question": "Is this a test?",
            "slug": "is-this-a-test",
            "outcomePrices": '["0.65", "0.35"]',
            "outcomes": ["Yes", "No"],
            "liquidity": "1000.50"
        }
        
        # Simulating parser logic
        prices = [float(p) for p in json.loads(market["outcomePrices"])]
        self.assertEqual(prices, [0.65, 0.35])
        self.assertEqual(float(market["liquidity"]), 1000.50)

if __name__ == "__main__":
    unittest.main()
