import time

from exchange_connector import get_client
from risk_manager import RiskManager
from execution_module import execute_orders
from strategies.spot_hft import SpotHFT
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest
from strategies.tri_arb import TriArbStrategy


def fetch_balance_info(client):
    bal = client.fetch_balance()
    total = bal.get("total", {})
    free_bal = bal.get("free", {})
    print("Вільний USDT:", free_bal.get("USDT", 0))
    return total, free_bal


def run_cycle(client, rm, spot, grid, ai, tri):
    total, free_bal = fetch_balance_info(client)
    free_usdt = free_bal.get("USDT", 0)

    # Spot-HFT
    ticker = client.fetch_ticker("BTC/USDT")
    bid = ticker["bid"]
    ask = ticker["ask"]
    s_signals = spot.generate_signals({"bid": bid, "ask": ask})
    s_filtered = rm.filter_signals(s_signals, total)
    execute_orders(client, s_filtered)

    # Grid
    g_signals = grid.generate_signals({"bid": bid, "ask": ask})
    g_filtered = rm.filter_signals(g_signals, total)
    execute_orders(client, g_filtered)

    # Auto-Invest
    multi = {
        s: {"price": client.fetch_ticker(s)["last"]}
        for s in ai.symbols
    }
    ai_signals = ai.generate_signals(multi, free_usdt)
    execute_orders(client, ai_signals)

    # Tri-Arb
    tri_data = {
        p: {
            "bid": client.fetch_ticker(p)["bid"],
            "ask": client.fetch_ticker(p)["ask"],
        }
        for p in tri.pairs
    }
    tri_signals = tri.generate_signals(tri_data, free_usdt)
    execute_orders(client, tri_signals)


def main():
    print("[DEBUG] orchestrator.py завантажено")
    client = get_client()

    rm = RiskManager({
        "risk.max_drawdown_pct": 0.05,
        "risk.daily_loss_limit": 0.02,
    })
    spot = SpotHFT(client, {"spread_threshold": 1e-7})
    grid = GridStrategy(client, {"levels": [-0.01, 0.01], "qty_pct": 0.01})
    ai = AutoInvest(
        client,
        {"symbols": ["BTC/USDT", "ETH/USDT"], "qty_pct": 0.005},
    )
    tri = TriArbStrategy(
        client,
        {
            "pairs": ["BTC/USDT", "ETH/USDT", "ETH/BTC"],
            "usdt_pct": 0.01,
            "min_profit": 0.01,
            "commission": 0.001,
        },
    )

    while True:
        run_cycle(client, rm, spot, grid, ai, tri)
        print("Очікуємо 60 сек…")
        time.sleep(60)


if __name__ == "__main__":
    main()
