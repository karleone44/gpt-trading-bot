import time
import yaml
from dotenv import load_dotenv

from exchange_connector import get_client
from risk_manager import RiskManager
from execution_module import execute_orders
from strategies.spot_hft import SpotHFT
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest
from strategies.tri_arb import TriArbStrategy
from strategies.ai_signals import AISignals
from strategies.rl_trader import RLTrader

def fetch_balance_info(client):
    bal = client.fetch_balance()
    total = bal.get("total", {})
    free_bal = bal.get("free", {})
    print("Вільний USDT:", free_bal.get("USDT", 0))
    return total, free_bal

def run_cycle(client, rm, spot, grid, auto, ai, tri, rl):
    total, free_bal = fetch_balance_info(client)
    free_usdt = free_bal.get("USDT", 0)

    # Spot-HFT
    ticker = client.fetch_ticker("BTC/USDT")
    bid, ask = ticker["bid"], ticker["ask"]
    s_signals = spot.generate_signals({"bid": bid, "ask": ask})
    execute_orders(client, rm.filter_signals(s_signals, total))

    # Grid Strategy
    g_signals = grid.generate_signals({"bid": bid, "ask": ask})
    execute_orders(client, rm.filter_signals(g_signals, total))

    # Auto-Invest
    prices = {s: {"price": client.fetch_ticker(s)["last"]} for s in auto.symbols}
    auto_signals = auto.generate_signals(prices, free_usdt)
    execute_orders(client, auto_signals)

    # AI-Signals
    ai_signals = ai.generate_signals(prices, free_usdt)
    execute_orders(client, ai_signals)

    # Triangular Arbitrage
    tri_data = {
        p: {"bid": client.fetch_ticker(p)["bid"], "ask": client.fetch_ticker(p)["ask"]}
        for p in tri.pairs
    }
    tri_signals = tri.generate_signals(tri_data, free_usdt)
    execute_orders(client, tri_signals)

    # RL-Trader
    rl_signals = rl.generate_signals(prices, free_usdt)
    execute_orders(client, rl_signals)

def main():
    print("[DEBUG] orchestrator.py завантажено")

    # Load environment variables and config
    load_dotenv("config/.env")
    with open("config/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    client = get_client()

    rm   = RiskManager(cfg.get("risk_manager", {}))
    spot = SpotHFT(client, cfg["strategies"]["spot_hft"])
    grid = GridStrategy(client, cfg["strategies"]["grid"])
    auto = AutoInvest(client, cfg["strategies"]["auto_invest"])
    ai   = AISignals(client, cfg["strategies"]["ai_signals"])
    tri  = TriArbStrategy(client, cfg["strategies"]["tri_arb"])
    rl   = RLTrader(client, cfg["strategies"]["rl_trader"])

    interval = cfg.get("orchestrator", {}).get("interval", 60)
    while True:
        run_cycle(client, rm, spot, grid, auto, ai, tri, rl)
        print(f"Очікуємо {interval} сек…")
        time.sleep(interval)

if __name__ == "__main__":
    main()
