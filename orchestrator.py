# orchestrator.py

from exchange_connector import get_client
from strategies.spot_hft import SpotHFT

def fetch_balance_info(client):
    balance = client.fetch_balance()
    total = balance.get('total', {})
    free  = balance.get('free', {})
    print("Вільний USDT:", free.get('USDT', 0))
    print("Загальний баланс:", total)

def main():
    client = get_client()

    # 1) Виводимо баланс
    fetch_balance_info(client)

    # 2) Ініціалізуємо Spot-HFT стратегію
    strategy = SpotHFT(client, {'spread_threshold': 0.001})

    # 3) Отримуємо ринкові дані
    ticker = client.fetch_ticker('BTC/USDT')
    print("Ринкові дані:", {'bid': ticker['bid'], 'ask': ticker['ask']})

    # 4) Генеруємо сигнали та виконуємо (тут — просто вивід)
    signals = strategy.generate_signals(ticker)
    print("Spot-HFT сигнали:", signals)

if __name__ == "__main__":
    main()
