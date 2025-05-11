# strategies/tri_arb.py

class TriArbStrategy:
    def __init__(self, client, config):
        self.client       = client
        # Порядок пар: [USDT→BTC, USDT←ETH, BTC→ETH]
        self.pairs        = config.get('pairs', ['BTC/USDT', 'ETH/USDT', 'ETH/BTC'])
        # Частка вільного USDT для арбітражу (наприклад, 1%)
        self.usdt_pct     = config.get('usdt_pct', 0.01)
        # Мінімальний прибуток (USDT), щоб робити угоду
        self.min_profit   = config.get('min_profit', 0.01)
        # Комісія на кожен ордер (0.001 = 0.1%)
        self.commission   = config.get('commission', 0.001)

    def generate_signals(self, data, free_usdt):
        """
        data: {
          'BTC/USDT': {'bid': ..., 'ask': ...},
          'ETH/BTC':  {'bid': ..., 'ask': ...},
          'ETH/USDT': {'bid': ..., 'ask': ...},
        }
        free_usdt: float
        """
        usdt_traded  = free_usdt * self.usdt_pct
        # Крок 1: USDT → BTC
        btc_amount   = usdt_traded / data['BTC/USDT']['ask']
        # Крок 2: BTC → ETH
        eth_amount   = btc_amount / data['ETH/BTC']['ask']
        # Крок 3: ETH → USDT
        gross_final  = eth_amount * data['ETH/USDT']['bid']
        # Вираховуємо чистий результат із урахуванням комісій (3 кроки)
        net_final    = gross_final * (1 - 3 * self.commission)
        profit       = net_final - usdt_traded

        # DEBUG
        print(f"[DEBUG TriArb] free_usdt={free_usdt:.6f}, pct={self.usdt_pct}")
        print(f"[DEBUG TriArb] usdt_traded={usdt_traded:.6f}")
        print(f"[DEBUG TriArb] btc_amount={btc_amount:.8f} @ ask={data['BTC/USDT']['ask']}")
        print(f"[DEBUG TriArb] eth_amount={eth_amount:.8f} @ ask={data['ETH/BTC']['ask']}")
        print(f"[DEBUG TriArb] gross_final={gross_final:.6f} @ bid={data['ETH/USDT']['bid']}")
        print(f"[DEBUG TriArb] net_final={net_final:.6f} after fees, profit={profit:.6f}")

        signals = []
        if profit >= self.min_profit:
            signals.append({
                'symbol': self.pairs[0],  # BTC/USDT
                'side':   'buy',
                'qty':    btc_amount,
                'price':  data['BTC/USDT']['ask'],
            })
            signals.append({
                'symbol': self.pairs[2],  # ETH/BTC
                'side':   'buy',
                'qty':    eth_amount,
                'price':  data['ETH/BTC']['ask'],
            })
            signals.append({
                'symbol': self.pairs[1],  # ETH/USDT
                'side':   'sell',
                'qty':    eth_amount,
                'price':  data['ETH/USDT']['bid'],
            })
        return signals
