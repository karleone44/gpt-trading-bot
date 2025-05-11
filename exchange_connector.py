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
    print("Баланс Spot:", balance.get('total'))
