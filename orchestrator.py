# orchestrator.py

from exchange_connector import get_client

def fetch_market():
    client = get_client()
    # приклад — отримати дані по парі BTC/USDT
    return client.fetch_ticker('BTC/USDT')

def generate_signals(data):
    # тимчасово — повертаємо порожній список сигналів
    return []

def execute_signals(signals):
    # поки просто логіруємо
    print("Сигнали:", signals)

def main():
    client = get_client()
    balance = client.fetch_balance()
    total = balance.get('total', {})
    free = balance.get('free', {})

    # Вивід балансу
    print("Вільний USDT:", free.get('USDT', 0))
    print("Загальний баланс:", total)

    # Fetch → Signal → Execute
    data = fetch_market()
    print("Ринкові дані:", data)

    signals = generate_signals(data)
    execute_signals(signals)

if __name__ == "__main__":
    main()
