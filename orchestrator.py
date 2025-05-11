# orchestrator.py

from exchange_connector import get_client
from strategies.spot_hft import SpotHFT
from risk_manager import RiskManager
from execution_module import execute_orders

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

    # 2) Ініціалізація Risk Manager
    rm = RiskManager({
        'risk.max_drawdown_pct': 0.05,
        'risk.daily_loss_limit': 0.02
    })
    rm.initialize(total)

    # 3) Ініціалізація Spot-HFT стратегії
    strategy = SpotHFT(client, {'spread_threshold': 0.0000001})

    # 4) Отримання ринкових даних по BTC/USDT
    ticker = client.fetch_ticker('BTC/USDT')
    bid = ticker['bid']
    ask = ticker['ask']
    print("Ринкові дані:", {'bid': bid, 'ask': ask})

    # 5) Генерація та фільтрація сигналів
    signals = strategy.generate_signals({'bid': bid, 'ask': ask})
    print("Spot-HFT сигнали (до ризику):", signals)
    filtered = rm.filter_signals(signals, total)
    print("Spot-HFT сигнали (після ризику):", filtered)

    # 6) Виконання фільтрованих сигналів
    execute_orders(client, filtered)

if __name__ == '__main__':
    main()
