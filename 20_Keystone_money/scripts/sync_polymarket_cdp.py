import json
import re
import urllib.request
import os
import datetime

BRAIN_ROOT = r"C:\Users\Curtis\Desktop\Keystone Brain"
TRACKER_PATH = os.path.join(BRAIN_ROOT, "20_Keystone_money", "hourly_flips_tracker.json")
LEDGER_MD_PATH = os.path.join(BRAIN_ROOT, "20_Keystone_money", "hourly_flips_ledger.md")
USER_WALLET = "0xbD7dCa5C890FC0Aa934E1681c0c8dA00A7689b03"

def sync_polymarket_portfolio():
    rate = 1.365
    cash_usd = 0.04
    portfolio_usd = None
    positions = []
    
    # --- LAYER 1: Official Polymarket Data API ---
    try:
        # 1. Fetch live positions
        pos_url = f"https://data-api.polymarket.com/positions?user={USER_WALLET}"
        req_pos = urllib.request.Request(pos_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_pos, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
        active = [p for p in data if float(p.get("size", 0)) > 0 and float(p.get("curPrice", 0)) > 0]
        for a in active:
            shares = float(a.get("size", 0))
            entry_price = float(a.get("avgPrice", 0))
            cur_price = float(a.get("curPrice", 0))
            val_usd = float(a.get("currentValue", 0)) or round(shares * cur_price, 2)
            stake_usd = round(shares * entry_price, 2)
            payout_usd = round(shares * 1.0, 2)
            
            pnl_val = val_usd - stake_usd
            pnl_pct = (pnl_val / stake_usd * 100.0) if stake_usd > 0 else 0.0
            pnl_str = f"{'+' if pnl_val >= 0 else '-'}${abs(pnl_val):.2f} ({abs(pnl_pct):.1f}%)"
            
            positions.append({
                "market": a.get("title", "WTA Match"),
                "side": a.get("outcome", "Underdog"),
                "shares": round(shares, 4),
                "size": round(shares, 4),
                "entry_odds": round(entry_price, 4),
                "cur_price": round(cur_price, 4),
                "current_mark": round(cur_price, 4),
                "stake_usd": stake_usd,
                "stake_cad": round(stake_usd * rate, 2),
                "potential_payout_usd": payout_usd,
                "potential_payout_cad": round(payout_usd * rate, 2),
                "value_usd": round(val_usd, 2),
                "value_cad": round(val_usd * rate, 2),
                "pnl_str": pnl_str,
                "status": "LIVE_ACTIVE",
                "action": "HOLD_TO_WIN",
                "asset_id": a.get("asset")
            })
            
        # 2. Fetch live portfolio value
        val_url = f"https://data-api.polymarket.com/value?user={USER_WALLET}"
        req_val = urllib.request.Request(val_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_val, timeout=5) as resp:
            val_data = json.loads(resp.read().decode("utf-8"))
            if isinstance(val_data, list) and len(val_data) > 0:
                portfolio_usd = float(val_data[0].get("value", 0))
    except Exception as e:
        print(f"Data API Warning: {e}")

    # --- LAYER 2: Chrome Port 9222 CDP Scrape for Rendered Cash & Portfolio ---
    try:
        tabs_req = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2)
        tabs = json.loads(tabs_req.read().decode("utf-8"))
        poly_tab = next((t for t in tabs if "polymarket.com" in t.get("url", "").lower()), None)
        if poly_tab and poly_tab.get("webSocketDebuggerUrl"):
            try:
                import websockets.sync.client as ws_sync
                with ws_sync.connect(poly_tab["webSocketDebuggerUrl"], close_timeout=2) as ws:
                    eval_msg = json.dumps({
                        "id": 1,
                        "method": "Runtime.evaluate",
                        "params": {"expression": "document.body.innerText", "returnByValue": True}
                    })
                    ws.send(eval_msg)
                    res = json.loads(ws.recv())
                    dom_text = res.get("result", {}).get("result", {}).get("value", "")
                    lines = [l.strip() for l in dom_text.split("\n") if l.strip()]
                    
                    for i, line in enumerate(lines):
                        if line == "Portfolio" and i + 1 < len(lines) and lines[i+1].startswith("$"):
                            try:
                                portfolio_usd = float(lines[i+1].replace("$", "").replace(",", ""))
                            except Exception:
                                pass
                        if (line in ("Cash", "Available to trade")) and i + 1 < len(lines) and lines[i+1].startswith("$"):
                            try:
                                cash_usd = float(lines[i+1].replace("$", "").replace(",", ""))
                            except Exception:
                                pass
            except Exception as ws_err:
                try:
                    import websocket
                    ws = websocket.create_connection(poly_tab["webSocketDebuggerUrl"], timeout=2)
                    eval_msg = json.dumps({
                        "id": 1,
                        "method": "Runtime.evaluate",
                        "params": {"expression": "document.body.innerText", "returnByValue": True}
                    })
                    ws.send(eval_msg)
                    res = json.loads(ws.recv())
                    ws.close()
                    dom_text = res.get("result", {}).get("result", {}).get("value", "")
                    lines = [l.strip() for l in dom_text.split("\n") if l.strip()]
                    for i, line in enumerate(lines):
                        if line == "Portfolio" and i + 1 < len(lines) and lines[i+1].startswith("$"):
                            try:
                                portfolio_usd = float(lines[i+1].replace("$", "").replace(",", ""))
                            except Exception:
                                pass
                        if (line in ("Cash", "Available to trade")) and i + 1 < len(lines) and lines[i+1].startswith("$"):
                            try:
                                cash_usd = float(lines[i+1].replace("$", "").replace(",", ""))
                            except Exception:
                                pass
                except Exception:
                    pass
    except Exception as e:
        print(f"CDP Scrape Warning: {e}")

    # --- Load Tracker ---
    tracker = {}
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8") as f:
                tracker = json.load(f)
            rate = tracker.get("usd_cad_exchange_rate", 1.365)
        except Exception:
            pass

    # Sum positions values if portfolio_usd was not scraped
    pos_sum_usd = round(sum(p.get("value_usd", 0.0) for p in positions), 2)
    if portfolio_usd is None or portfolio_usd <= 0:
        portfolio_usd = pos_sum_usd
    else:
        portfolio_usd = round(portfolio_usd, 2)

    total_payout_usd = round(sum(p.get("potential_payout_usd", 0.0) for p in positions), 2)
    cash_cad = round(cash_usd * rate, 2)
    portfolio_cad = round(portfolio_usd * rate, 2)
    total_nav_usd = round(portfolio_usd + cash_usd, 2)
    total_nav_cad = round(total_nav_usd * rate, 2)
    fortress_cad = round(total_nav_cad * 0.40, 2)
    fortress_usd = round(total_nav_usd * 0.40, 2)
    active_float_cad = cash_cad
    active_float_usd = cash_usd
    next_stake_cad = round(cash_cad / 3.0, 2)
    next_stake_usd = round(cash_usd / 3.0, 2)
    total_payout_cad = round(total_payout_usd * rate, 2)

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    tracker.update({
        "date": today_str,
        "last_update": now_iso,
        "last_updated": now_iso,
        "base_currency": "CAD",
        "currency_base": "CAD",
        "usd_cad_exchange_rate": rate,
        "wallet_address": USER_WALLET,
        "liquid_cash_usd": cash_usd,
        "current_cash_usd": cash_usd,
        "cash_balance_usd": cash_usd,
        "current_cash_cad": cash_cad,
        "cash_balance_cad": cash_cad,
        "money_out_in_play_usd": portfolio_usd,
        "money_out_in_play_cad": portfolio_cad,
        "portfolio_positions_value_usd": portfolio_usd,
        "portfolio_positions_value_cad": portfolio_cad,
        "current_portfolio_usd": portfolio_usd,
        "current_portfolio_cad": portfolio_cad,
        "portfolio_nav_usd": total_nav_usd,
        "portfolio_nav_cad": total_nav_cad,
        "total_account_nav_usd": total_nav_usd,
        "total_account_nav_cad": total_nav_cad,
        "cash_reserve_floor_cad": fortress_cad,
        "cash_reserve_floor_usd": fortress_usd,
        "active_float_cad": active_float_cad,
        "active_float_usd": active_float_usd,
        "next_stake_cad": next_stake_cad,
        "next_stake_usd": next_stake_usd,
        "total_potential_payout_usd": total_payout_usd,
        "total_potential_payout_cad": total_payout_cad,
        "open_positions": positions,
        "existing_portfolio_positions": positions
    })

    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=2)

    # --- Update Markdown Ledger ---
    try:
        update_markdown_ledger(tracker, positions, now_iso)
    except Exception as e:
        print(f"Ledger MD Error: {e}")

    # --- Trigger Keystone Studio UI Live Refresh ---
    try:
        refresh_keystone_studio_ui(tracker)
    except Exception as e:
        print(f"CDP Studio UI Refresh notice: {e}")

    result_payload = {
        "status": "SYNCED",
        "cash_usd": cash_usd,
        "cash_cad": cash_cad,
        "portfolio_usd": portfolio_usd,
        "portfolio_cad": portfolio_cad,
        "total_nav_usd": total_nav_usd,
        "total_nav_cad": total_nav_cad,
        "cash_fortress_cad": fortress_cad,
        "total_potential_payout_usd": total_payout_usd,
        "total_potential_payout_cad": total_payout_cad,
        "positions_count": len(positions),
        "positions": positions
    }
    return result_payload, None


def update_markdown_ledger(tracker, positions, now_iso):
    if not os.path.exists(LEDGER_MD_PATH):
        return
        
    with open(LEDGER_MD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    rate = tracker.get("usd_cad_exchange_rate", 1.365)
    nav_cad = tracker.get("total_account_nav_cad", 19.49)
    nav_usd = tracker.get("total_account_nav_usd", 14.28)
    fortress_cad = tracker.get("cash_reserve_floor_cad", 7.80)
    cash_cad = tracker.get("current_cash_cad", 0.05)
    cash_usd = tracker.get("liquid_cash_usd", 0.04)
    payout_usd = tracker.get("total_potential_payout_usd", 78.83)
    payout_cad = tracker.get("total_potential_payout_cad", 107.60)

    header = f"\n\n### 🎾 Live WTA 3-Bet Swarm Slate — {tracker.get('date')} ({now_iso[:16]} UTC)\n"
    header += f"- **Total Account NAV**: ${nav_cad:.2f} CAD (${nav_usd:.2f} USD) | **40% Fortress Floor**: ${fortress_cad:.2f} CAD [LOCKED 🔒]\n"
    header += f"- **Liquid Cash Balance**: ${cash_cad:.2f} CAD (${cash_usd:.2f} USD) | **Portfolio in Play**: ${tracker.get('money_out_in_play_cad', 19.44):.2f} CAD (${tracker.get('money_out_in_play_usd', 14.24):.2f} USD)\n"
    header += f"- **Total Potential Payout**: **${payout_cad:.2f} CAD** (**${payout_usd:.2f} USD**)\n\n"
    header += "| # | Tournament & Matchup | Selection (Dog) | Shares | Entry Price | Current Mark | Value (USD / CAD) | Potential Return (USD / CAD) | Status |\n"
    header += "|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|\n"

    for idx, pos in enumerate(positions, 1):
        m = pos.get("market", "")
        s = pos.get("side", "")
        sh = pos.get("shares", 0)
        e = pos.get("entry_odds", 0) * 100
        cm = pos.get("current_mark", 0) * 100
        v_usd = pos.get("value_usd", 0)
        v_cad = pos.get("value_cad", 0)
        p_usd = pos.get("potential_payout_usd", 0)
        p_cad = pos.get("potential_payout_cad", 0)
        header += f"| {idx} | {m} | **{s}** | {sh:.1f} | {e:.1f}¢ | {cm:.1f}¢ | ${v_usd:.2f} (${v_cad:.2f}) | **${p_usd:.2f} (${p_cad:.2f})** | **{pos.get('status')}** |\n"

    content += header
    with open(LEDGER_MD_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def refresh_keystone_studio_ui(tracker):
    try:
        tabs_req = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2)
        tabs = json.loads(tabs_req.read().decode("utf-8"))
        studio_tab = next((t for t in tabs if "keystone_tauri_next" in t.get("url", "") or "keystone studio" in t.get("title", "").lower()), None)
        if studio_tab and studio_tab.get("webSocketDebuggerUrl"):
            import websockets.sync.client as ws_sync
            with ws_sync.connect(studio_tab["webSocketDebuggerUrl"], close_timeout=2) as ws:
                js_reload = f"""
                if (window.loadWtaMoneyDeck) {{
                    window.loadWtaMoneyDeck();
                }}
                if (window.keystoneLogTerminal) {{
                    window.keystoneLogTerminal('🔄 [Polymarket Sync] Port 9222 Sync: Portfolio ${tracker.get("money_out_in_play_cad"):.2f} CAD, Cash ${tracker.get("current_cash_cad"):.2f} CAD, NAV ${tracker.get("total_account_nav_cad"):.2f} CAD.');
                }}
                """
                msg = json.dumps({
                    "id": 1,
                    "method": "Runtime.evaluate",
                    "params": {"expression": js_reload, "returnByValue": True}
                })
                ws.send(msg)
    except Exception as e:
        print(f"CDP Studio UI Refresh notice: {e}")


if __name__ == "__main__":
    res, err = sync_polymarket_portfolio()
    print("Polymarket Sync Success:", json.dumps(res, indent=2))
