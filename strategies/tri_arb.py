# strategies/tri_arb.py

class TriArbStrategy:
    def __init__(self, client, config):
        self.client    = client
        self.pairs     = config.get('pairs', ['BTC/USDT', 'ETH/USDT', 'ETH/BTC'])
        self.usdt_pct  = config.get('usdt_pct', 0.01)

    def generate_signals(self, data, free_usdt):
        """
        data: dict з ticker’ами для self.pairs, кожен має 'bid' і 'ask'
        free_usdt: float
        """
        # Кроки арбітражу
        usdt_to_trade = free_usdt * self.usdt_pct
        btc_amount    = usdt_to_trade / data['BTC/USDT']['ask']
        eth_amount    = btc_amount      / data['ETH/BTC']['ask']
        final_usdt    = eth_amount      * data['ETH/USDT']['bid']
        profit        = final_usdt - usdt_to_trade

        # DEBUG: покажемо всі проміжні значення
        print(f"[DEBUG TriArb] free_usdt={free_usdt}, usdt_pct={self.usdt_pct}")
        print(f"[DEBUG TriArb] usdt_to_trade={usdt_to_trade:.8f}")
        print(f"[DEBUG TriArb] btc_amount={btc_amount:.8f}  (at ask={data['BTC/USDT']['ask']})")
        print(f"[DEBUG TriArb] eth_amount={eth_amount:.8f}  (at ask={data['ETH/BTC']['ask']})")
        print(f"[DEBUG TriArb] final_usdt={final_usdt:.8f}  (at bid={data['ETH/USDT']['bid']})")
        print(f"[DEBUG TriArb] profit={profit:.8f}")

        signals = []
        if profit > 0:
            signals.append({
                'symbol': 'BTC/USDT',
                'side':   'buy',
                'qty':    btc_amount,
                'price':  data['BTC/USDT']['ask'],
            })
            signals.append({
                'symbol': 'ETH/BTC',
                'side':   'buy',
                'qty':    eth_amount,
                'price':  data['ETH/BTC']['ask'],
            })
            signals.append({
                'symbol': 'ETH/USDT',
                'side':   'sell',
                'qty':    eth_amount,
                'price':  data['ETH/USDT']['bid'],
            })
        return signals
