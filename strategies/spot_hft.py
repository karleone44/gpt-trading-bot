import logging

class SpotHFT:
    def __init__(self, client, config):
        self.client = client
        # гарантовано float
        try:
            self.threshold = float(config['spread_threshold'])
        except (KeyError, ValueError) as e:
            logging.error(f"Invalid spread_threshold in config: {config.get('spread_threshold')}")
            raise
        logging.debug(f"SpotHFT threshold set to {self.threshold}")

    def generate_signals(self, ticker):
        # перетворюємо bid/ask у float
        try:
            bid = float(ticker['bid'])
            ask = float(ticker['ask'])
        except (KeyError, ValueError, TypeError) as e:
            logging.error(f"Invalid ticker data: {ticker}")
            return []

        spread = (ask - bid) / bid
        logging.debug(f"SpotHFT computed spread: {spread} (threshold: {self.threshold})")

        if spread < self.threshold:
            logging.info(f"Spread {spread:.6f} below threshold; generating BUY signal")
            return [{
                "side": "buy",    # ключ "side" для ExecutionModule
                "price": bid
            }]
        return []
