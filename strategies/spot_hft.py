# strategies/spot_hft.py
class SpotHFT:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def generate_signals(self, data):
        bid       = data['bid']
        ask       = data['ask']
        spread    = (ask - bid) / ask
        threshold = self.config.get('spread_threshold', 0.001)

        # Debug - вивід значень
        print(f"[DEBUG] bid={bid}, ask={ask}, spread={spread:.6f}, threshold={threshold}")

        signals = []
        if spread <= threshold:
            signals.append({'side': 'buy', 'price': ask})
        elif spread >= threshold:
            signals.append({'side': 'sell', 'price': bid})
        return signals
