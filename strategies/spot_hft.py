class SpotHFT:
    """C1: High-frequency spot strategy."""

    def __init__(self, client, config):
        self.client = client
        self.threshold = config.get("spread_threshold", 1e-7)

    def generate_signals(self, data):
        bid = data["bid"]
        ask = data["ask"]
        spread = (ask - bid) / ask

        # Купуємо тільки якщо спред строго менший за поріг
        if spread < self.threshold:
            return [
                {
                    "symbol": "BTC/USDT",
                    "side": "buy",
                    "price": ask,
                    "qty": None,
                }
            ]

        # Якщо спред більший або рівний порогу — продаємо
        if spread >= self.threshold:
            return [
                {
                    "symbol": "BTC/USDT",
                    "side": "sell",
                    "price": bid,
                    "qty": None,
                }
            ]

        return []
