# exchange_connector.py

from dotenv import load_dotenv
import os, ccxt

# Підвантажуємо змінні з .env (де лежать ваші API-ключі)
load_dotenv()

def get_client():
    return ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET'),
        'enableRateLimit': True,
    })

if __name__ == '__main__':
    client = get_client()
    print(client.fetch_balance())
