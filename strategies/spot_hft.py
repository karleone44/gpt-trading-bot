# strategies/spot_hft.py
class SpotHFT:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def generate_signals(self, ticker_data):
        bid = ticker_data['bid']
        ask = ticker_data['ask']
        spread = (ask - bid) / ask
        threshold = self.config.get('spread_threshold', 0.001)
        signals = []
        if spread <= threshold:
            signals.append({'side': 'buy', 'price': ask})
        elif spread >= threshold:
            signals.append({'side': 'sell', 'price': bid})
        return signals
