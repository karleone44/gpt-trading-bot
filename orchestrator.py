# orchestrator.py
import time
import yaml
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
from dotenv import load_dotenv

from exchange_manager import ExchangeManager
from risk_manager import RiskManager
from execution_module import execute_orders

from strategies.spot_hft import SpotHFT
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest
from strategies.tri_arb import TriArbStrategy
from strategies.delta_neutral import DeltaNeutralStrategy
from strategies.ai_signals import AISignals
#from strategies.rl_trader import RLTraderStrategy

load_dotenv("config/.env")

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def fetch_balance_info(client):
    bal = client.fetch_balance()
    total = bal.get("total", {})
    free = bal.get("free", {})
    print("Вільний USDT:", free.get("USDT", 0))
    return total, free


def fetch_market_snapshot(client):
    # Повертає словник ticker-даних для усіх необхідних пар
    symbols = ["BTC/USDT", "ETH/USDT"]
    snapshot = {}
    for sym in symbols:
        t = client.fetch_ticker(sym)
        snapshot[sym] = {"bid": t["bid"], "ask": t["ask"], "last": t.get("last")}
    return snapshot


def run_cycle(client, rm, spot, grid, auto, ai, tri, dn):
    # 1. Баланси
    total_bal, free_bal = fetch_balance_info(client)
    free_usdt = free_bal.get("USDT", 0)

    # 2. Формуємо список пар для арбітражу з конфігурації TriArbStrategy
    pairs = tri.pairs  # наприклад ["BTC/USDT","ETH/USDT","ETH/BTC"]

    # 3. Збір ринкових даних лише по цим парам
    market_snapshot = {}
    for pair in pairs:
        ticker = client.fetch_ticker(pair)
        market_snapshot[pair] = {
            "bid": float(ticker["bid"]),
            "ask": float(ticker["ask"]),
            "last": float(ticker["last"])
        }

    # 4. Генеруємо сигнали
    signals = []

    # 4.1 Spot-HFT та Grid тільки для USDT пар
    usdt_pairs = [p for p in pairs if p.endswith("/USDT")]
    for pair in usdt_pairs:
        data = market_snapshot[pair]
        signals += spot.generate_signals(data)
        signals += grid.generate_signals(data)

    # 4.2 Auto-Invest: передаємо ціни лише USDT пар
    prices = {p: {"price": market_snapshot[p]["last"]} for p in usdt_pairs}
    signals += auto.generate_signals(prices, free_usdt)

    # 4.3 AI-Signals: вся карта даних
    signals += ai.generate_signals(market_snapshot, free_usdt)

    # 4.4 Triangular Arbitrage: та сама карта
    signals += tri.generate_signals(market_snapshot, free_usdt)

    # 4.5 Delta-Neutral: теж
    signals += dn.generate_signals(market_snapshot, free_usdt)


    # 5. Фільтрація сигналів і виконання ордерів
    filtered = rm.filter_signals(signals, total_bal)
    valid = [s for s in filtered if isinstance(s, dict) and 'side' in s]
    execute_orders(client, valid)



def main():
    print(">>> ORCHESTRATOR started ", flush=True)
    cfg = load_config("config/config.yaml")
    exch_mgr = ExchangeManager(cfg)
    client = exch_mgr.get("binance")
    rm = RiskManager(cfg.get("risk_manager", {}))

    # Ініціалізація стратегій
    spot = SpotHFT(client, cfg["strategies"]["spot_hft"])
    grid = GridStrategy(client, cfg["strategies"]["grid"])
    auto = AutoInvest(client, cfg["strategies"]["auto_invest"])
    ai = AISignals(cfg["strategies"]["ai_signals"])
    tri = TriArbStrategy(client, cfg["strategies"]["tri_arb"])
    dn = DeltaNeutralStrategy(client, cfg["strategies"]["delta_neutral"])
   #rl = RLTraderStrategy(client, cfg["strategies"]["rl_trader"])

    interval = cfg.get("orchestrator", {}).get("interval", 60)
    logging.debug("orchestrator.py завантажено")
    while True:
        try:
            run_cycle(client, rm, spot, grid, auto, ai, tri, dn)
        except Exception as e:
            logging.error(f"Error in run_cycle: {e}")
        print(f"Очікуємо {interval} сек…")
        time.sleep(interval)

if __name__ == "__main__":
    main()
