from dotenv import load_dotenv
import os
import ccxt


load_dotenv()


def get_client():
    return ccxt.binance({
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET"),
        "enableRateLimit": True,
    })


if __name__ == "__main__":
    print(get_client().fetch_balance())
