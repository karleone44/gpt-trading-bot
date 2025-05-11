# orchestrator.py

import time
from exchange_connector import get_client
from strategies.spot_hft import SpotHFT
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest
from strategies.tri_arb import TriArbStrategy
from risk_manager import RiskManager
from execution_module import execute_orders

print("[DEBUG] orchestrator.py завантажено")

def fetch_balance_info(client):
    bal = client.fetch_balance()
    total = bal.get('total', {})
    free  = bal.get('free', {})
    print("Вільний USDT:", free.get('USDT', 0))
    return total, free

def run_cycle(client, rm, spot, grid, ai, tri):
    total, free = fetch_balance_info(client)
    free_usdt = free.get('USDT', 0)

    # Spot-HFT
    t = client.fetch_ticker('BTC/USDT')
    bid, ask = t['bid'], t['ask']
    print("Spot-HFT market:", {'bid': bid, 'ask': ask})
    s_signals = spot.generate_signals({'bid': bid, 'ask': ask})
    f_signals = rm.filter_signals(s_signals, total)
    execute_orders(client, f_signals)

    # Grid
    g_signals = grid.generate_signals({'bid': bid, 'ask': ask})
    gf = rm.filter_signals(g_signals, total)
    execute_orders(client, gf)

    # Auto-Invest
    multi = {sym: {'price': client.fetch_ticker(sym)['last']} for sym in ai.symbols}
    ai_signals = ai.generate_signals(multi, free_usdt)
    execute_orders(client, ai_signals)

    # Tri-Arb
    tri_data = {
        p: {'bid': client.fetch_ticker(p)['bid'], 'ask': client.fetch_ticker(p)['ask']}
        for p in tri.pairs
    }
    tri_signals = tri.generate_signals(tri_data, free_usdt)
    execute_orders(client, tri_signals)

def main():
    print("Старт Orchestrator")
    client = get_client()

    rm   = RiskManager({'risk.max_drawdown_pct': 0.05, 'risk.daily_loss_limit': 0.02})
    spot = SpotHFT(client, {'spread_threshold': 0.0000001})
    grid = GridStrategy(client, {'levels': [-0.01, 0.01], 'qty_pct': 0.01})
    ai   = AutoInvest(client, {'symbols': ['BTC/USDT', 'ETH/USDT'], 'qty_pct': 0.005})
    tri  = TriArbStrategy(client, {
        'pairs':      ['BTC/USDT', 'ETH/USDT', 'ETH/BTC'],
        'usdt_pct':   0.01,
        'min_profit': 0.01,
        'commission': 0.001,
    })

    interval = 60  # секунд між циклами
    while True:
        run_cycle(client, rm, spot, grid, ai, tri)
        print(f"Очікуємо {interval} секунд до наступного циклу...\n")
        time.sleep(interval)

if __name__ == '__main__':
    main()
