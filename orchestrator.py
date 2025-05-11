# orchestrator.py

from exchange_connector import get_client
from strategies.spot_hft import SpotHFT
from risk_manager import RiskManager
from execution_module import execute_orders
from strategies.grid import GridStrategy
from strategies.auto_invest import AutoInvest

# DEBUG: перевірка, що файл завантажився
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

    # 1) Баланс
    total, free = fetch_balance_info(client)
    free_usdt = free.get('USDT', 0)

    # 2) Risk Manager
    rm = RiskManager({
        'risk.max_drawdown_pct': 0.05,
        'risk.daily_loss_limit': 0.02
    })
    rm.initialize(total)

    # 3) Spot-HFT Strategy
    strategy = SpotHFT(client, {'spread_threshold': 0.0000001})
    ticker = client.fetch_ticker('BTC/USDT')
    bid = ticker['bid']
    ask = ticker['ask']
    print("Ринкові дані:", {'bid': bid, 'ask': ask})

    signals = strategy.generate_signals({'bid': bid, 'ask': ask})
    print("Spot-HFT сигнали (до ризику):", signals)
    filtered = rm.filter_signals(signals, total)
    print("Spot-HFT сигнали (після ризику):", filtered)
    execute_orders(client, filtered)

    # 4) Grid Strategy
    grid = GridStrategy(client, {'levels': [-0.01, 0.01], 'qty_pct': 0.01})
    grid_signals = grid.generate_signals({'bid': bid, 'ask': ask})
    print("Grid сигнали (до ризику):", grid_signals)
    grid_filtered = rm.filter_signals(grid_signals, total)
    print("Grid сигнали (після ризику):", grid_filtered)
    execute_orders(client, grid_filtered)

    # 5) Auto-Invest Strategy
    ai = AutoInvest(client, {
        'symbols': ['BTC/USDT', 'ETH/USDT'],
        'qty_pct': 0.005
    })
    # Збираємо останню ціну для кожної монети
    multi_ticker = {}
    for sym in ai.symbols:
        t = client.fetch_ticker(sym)
        multi_ticker[sym] = {'price': t['last']}
    ai_signals = ai.generate_signals(multi_ticker, free_usdt)
    print("Auto-Invest сигнали:", ai_signals)
    execute_orders(client, ai_signals)

if __name__ == '__main__':
    main()
