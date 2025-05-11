# exchange_connector.py
import os, ccxt

def get_client():
    return ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET'),
        'enableRateLimit': True
    })

if __name__ == "__main__":
    client = get_client()
    balance = client.fetch_balance()
    total = balance.get('total', {})
    free = balance.get('free', {})
    # Виводимо повний баланс всіх активів
    print("Повний баланс:", total)
    # Виводимо вільний (available) баланс USDT
    print("Вільний баланс USDT:", free.get('USDT', 0))
