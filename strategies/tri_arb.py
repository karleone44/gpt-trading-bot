class TriArbStrategy:
    """C7: Triangular Arbitrage Strategy"""

    def __init__(self, client, config):
        self.client = client
        self.pairs = config['pairs']
        self.usdt_pct = config['usdt_pct']
        self.min_profit = config['min_profit']
        self.commission = config['commission']

    def generate_signals(self, data, free_usdt):
        ut = free_usdt * self.usdt_pct
        btc = ut / data['BTC/USDT']['ask']
        eth = btc / data['ETH/BTC']['ask']
        gross = eth * data['ETH/USDT']['bid']
        net = gross * (1 - 3 * self.commission)

        profit = net - ut

        print(
            f"[DEBUG TriArb] ut={ut:.6f}, "
            f"btc={btc:.8f}, "
            f"eth={eth:.8f}, "
            f"gross={gross:.6f}, "
            f"net={net:.6f}, "
            f"profit={profit:.6f}"
        )

        if profit >= self.min_profit:
            return [
                {
                    'symbol': 'BTC/USDT',
                    'side': 'buy',
                    'price': data['BTC/USDT']['ask'],
                    'qty': btc,
                },
                {
                    'symbol': 'ETH/BTC',
                    'side': 'buy',
                    'price': data['ETH/BTC']['ask'],
                    'qty': eth,
                },
                {
                    'symbol': 'ETH/USDT',
                    'side': 'sell',
                    'price': data['ETH/USDT']['bid'],
                    'qty': eth,
                },
            ]

        return []
