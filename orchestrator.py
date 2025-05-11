# orchestrator.py
from exchange_connector import get_client
from strategies.spot_hft import SpotHFT

def main():
    client = get_client()
    # Баланс
    balance = client.fetch_balance()
    free = balance.get('free', {})
    total = balance.get('total', {})
    print("Вільний USDT:", free.get('USDT', 0))
    print("Загальний баланс:", total)

    # Ініціалізація стратегії
    strategy = SpotHFT(client, {'spread_threshold': 0.001})

    # Fetch
    ticker = client.fetch_ticker('BTC/USDT')
    print("Ринкові дані:", {'bid': ticker['bid'], 'ask': ticker['ask']})

    # Generate & Execute
    signals = strategy.generate_signals(ticker)
    print("Spot-HFT сигнали:", signals)

if __name__ == '__main__':
    main()
