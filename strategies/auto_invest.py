# strategies/auto_invest.py

class AutoInvest:
    def __init__(self, client, config):
        self.client = client
        # список монет, наприклад ['BTC', 'ETH', 'BNB']
        self.symbols = config.get('symbols', ['BTC/USDT', 'ETH/USDT'])
        # відсоток вільного USDT на кожну монету
        self.qty_pct = config.get('qty_pct', 0.005)

    def generate_signals(self, data, free_usdt):
        signals = []
        for symbol in self.symbols:
            price = data.get(symbol, {}).get('price')
            if price:
                amount = free_usdt * self.qty_pct
                qty = amount / price
                signals.append({'symbol': symbol, 'side': 'buy', 'price': price, 'qty': qty})
        return signals
