# strategies/grid.py

class GridStrategy:
    def __init__(self, client, config):
        self.client = client
        self.levels = config.get('levels', [-0.01, 0.01])
        self.qty_pct = config.get('qty_pct', 0.01)

    def generate_signals(self, data):
        bid = data['bid']
        ask = data['ask']
        mid = (bid + ask) / 2
        signals = []
        for pct in self.levels:
            price = mid * (1 + pct)
            side = 'buy' if pct < 0 else 'sell'
            signals.append({'side': side, 'price': price, 'qty_pct': self.qty_pct})
        return signals
