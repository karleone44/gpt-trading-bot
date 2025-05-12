import os

from dotenv import load_dotenv
import ccxt


load_dotenv()


def get_client():
    """Returns a configured CCXT Binance client."""
    return ccxt.binance({
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET"),
        "enableRateLimit": True,
    })


if __name__ == "__main__":
    client = get_client()
    print(client.fetch_balance())
