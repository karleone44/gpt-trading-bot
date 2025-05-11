# orchestrator.py

from exchange_connector import get_client
from strategies.spot_hft import SpotHFT
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest
from strategies.tri_arb import TriArbStrategy
from risk_manager import RiskManager
from execution_module import execute_orders

print("[DEBUG] orchestrator.py завантажено")

def fetch_balance_info(client):
    balance = client.fetch_balance()
    total   = balance.get('total', {})
    free    = balance.get('free', {})
    print("Вільний USDT:", free.get('USDT', 0))
    print("Загальний баланс:", total)
    return total, free

def main():
    print("Старт Orchestrator")
    client = get_client()
    total, free = fetch_balance_info(client)
    free_usdt = free.get('USDT', 0)

    rm = RiskManager({'risk.max_drawdown_pct': 0.05, 'risk.daily_loss_limit': 0.02})
    rm.initialize(total)

    # Spot-HFT
    spot = SpotHFT(client, {'spread_threshold': 0.0000001})
    t = client.fetch_ticker('BTC/USDT')
    bid, ask = t['bid'], t['ask']
    print("Ринок:", {'bid': bid, 'ask': ask})
    signals = spot.generate_signals({'bid': bid, 'ask': ask})
    print("Spot-HFT до ризику:", signals)
    f = rm.filter_signals(signals, total)
    print("Spot-HFT після ризику:", f)
    execute_orders(client, f)

    # Grid
    grid = GridStrategy(client, {'levels': [-0.01, 0.01], 'qty_pct': 0.01})
    gs = grid.generate_signals({'bid': bid, 'ask': ask})
    print("Grid до ризику:", gs)
    gf = rm.filter_signals(gs, total)
    print("Grid після ризику:", gf)
    execute_orders(client, gf)

    # Auto-Invest
    ai = AutoInvest(client, {'symbols': ['BTC/USDT','ETH/USDT'], 'qty_pct': 0.005})
    multi = {}
    for sym in ai.symbols:
        tick = client.fetch_ticker(sym)
        multi[sym] = {'price': tick['last']}
    ai_sig = ai.generate_signals(multi, free_usdt)
    print("Auto-Invest сигнали:", ai_sig)
    execute_orders(client, ai_sig)

    # Tri-Arb
    tri = TriArbStrategy(client, {
        'pairs': ['BTC/USDT','ETH/USDT','ETH/BTC'],
        'usdt_pct': 0.01
    })
    data = {}
    for p in tri.pairs:
        tt = client.fetch_ticker(p)
        data[p] = {'bid': tt['bid'], 'ask': tt['ask']}
    tri_sig = tri.generate_signals(data, free_usdt)
    print("Tri-Arb сигнали:", tri_sig)
    execute_orders(client, tri_sig)

if __name__ == '__main__':
    main()
