# orchestrator.py
import time
from exchange_connector import get_client

def fetch_market():
    client = get_client()
    # приклад: тільки пара BTC/USDT
    return client.fetch_ticker('BTC/USDT')

def generate_signals(data):
    # тимчасово — ніяких сигналів
    return []

def execute_signals(signals):
    print("Сигнали:", signals)

def main():
    print("Старт Orchestrator")
    data = fetch_market()
    print("Ринкові дані:", data)
    signals = generate_signals(data)
    execute_signals(signals)

if __name__ == "__main__":
    main()
