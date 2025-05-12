# strategies/auto_invest.py

class AutoInvest:
    def __init__(self, client, config):
        self.client = client
        # список торгових пар для DCA
        self.symbols = config.get('symbols', ['BTC/USDT', 'ETH/USDT'])
        # частка вільного USDT на кожну покупку (наприклад, 0.5%)
        self.qty_pct = config.get('qty_pct', 0.005)

    def generate_signals(self, data, free_usdt):
        """
        data: dict, ключі — символи, значення — {'price': last_price}
        free_usdt: float, вільний USDT
        """
        signals = []
        for symbol in self.symbols:
            info = data.get(symbol)
            price = info.get('price') if info else None
            if price and free_usdt > 0:
                amount = free_usdt * self.qty_pct
                qty = amount / price
                signals.append({
                    'symbol': symbol,
                    'side': 'buy',
                    'price': price,
                    'qty': qty
                })
        return signals
