# orchestrator.py

from exchange_connector import get_client
from strategies.spot_hft import SpotHFT

def fetch_balance_info(client):
    balance = client.fetch_balance()
    total   = balance.get('total', {})
    free    = balance.get('free', {})
    print("Вільний USDT:", free.get('USDT', 0))
    print("Загальний баланс:", total)

def main():
    print("Старт Orchestrator")
    client = get_client()

    # 1) Вивід балансу
    fetch_balance_info(client)

    # 2) Ініціалізація Spot-HFT стратегії
    strategy = SpotHFT(client, {'spread_threshold': 0.001})

    # 3) Отримання ринкових даних
    ticker = client.fetch_ticker('BTC/USDT')
    bid = ticker['bid']
    ask = ticker['ask']
    print("Ринкові дані:", {'bid': bid, 'ask': ask})

    # 4) Генерація Spot-HFT сигналів
    signals = strategy.generate_signals({'bid': bid, 'ask': ask})
    print("Spot-HFT сигнали:", signals)

if __name__ == '__main__':
    main()
