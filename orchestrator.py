# orchestrator.py

import os
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

def fetch_balance_info(client):
    """Отримати загальний та вільний баланс USDT."""
    bal = client.fetch_balance()
    total = bal.get("total", {})
    free_bal = bal.get("free", {})
    print("Вільний USDT:", free_bal.get("USDT", 0))
    return total, free_bal

def run_cycle(client, rm, spot, grid, auto, ai, tri):
    """
    Один цикл роботи:
      1) Spot-HFT
      2) Grid
      3) Auto-Invest
      4) AI-Signals (GPT)
      5) Tri-Arb
    """
    total, free_bal = fetch_balance_info(client)
    free_usdt = free_bal.get("USDT", 0)

    # 1) Spot-HFT
    ticker = client.fetch_ticker("BTC/USDT")
    bid, ask = ticker["bid"], ticker["ask"]
    s_signals = spot.generate_signals({"bid": bid, "ask": ask})
    s_filtered = rm.filter_signals(s_signals, total)
    execute_orders(client, s_filtered)

    # 2) Grid Strategy
    g_signals = grid.generate_signals({"bid": bid, "ask": ask})
    g_filtered = rm.filter_signals(g_signals, total)
    execute_orders(client, g_filtered)

    # 3) Auto-Invest DCA
    prices = {s: {"price": client.fetch_ticker(s)["last"]} for s in auto.symbols}
    auto_signals = auto.generate_signals(prices, free_usdt)
    execute_orders(client, auto_signals)

    # 4) AI-Signals via GPT
    ai_signals = ai.generate_signals(prices, free_usdt)
    execute_orders(client, ai_signals)

    # 5) Triangular Arbitrage
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
    """Точка входу: завантажуємо налаштування, ініціалізуємо модулі та запускаємо цикл."""
    print("[DEBUG] orchestrator.py завантажено")

    # 1. Завантажити змінні середовища з config/.env
    load_dotenv("config/.env")

    # 2. Зчитати YAML-конфіг
    with open("config/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    # 3. Під’єднатися до біржі
    client = get_client()

    # 4. Ініціалізувати всі модулі зі своїми секціями конфігурації
    rm    = RiskManager(cfg.get("risk_manager", {}))
    spot  = SpotHFT(client, cfg["strategies"]["spot_hft"])
    grid  = GridStrategy(client, cfg["strategies"]["grid"])
    auto  = AutoInvest(client, cfg["strategies"]["auto_invest"])
    ai    = AISignals(client, cfg["strategies"]["ai_signals"])
    tri   = TriArbStrategy(client, cfg["strategies"]["tri_arb"])

    # 5. Інтервал циклу (секунди)
    interval = cfg.get("orchestrator", {}).get("interval", 60)

    # 6. Нескінченний цикл
    while True:
        run_cycle(client, rm, spot, grid, auto, ai, tri)
        print(f"Очікуємо {interval} сек…")
        time.sleep(interval)

if __name__ == "__main__":
    main()
