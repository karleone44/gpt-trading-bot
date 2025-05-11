class DeltaNeutralStrategy:
    """
    C8: Delta-Neutral Strategy
    Розміщує одночасні long/short позиції у двох активах
    згідно з hedge_ratio та аналізу price spread.
    """
    def __init__(self, client, config):
        self.client = client
        self.window = config.get("window", 60)
        self.hedge_ratio = config.get("hedge_ratio", 0.5)

    def generate_signals(self, data, free_usdt):
        """
        data: {
          'ASSET1/USDT': {'bid': .., 'ask': ..},
          'ASSET2/USDT': {'bid': .., 'ask': ..},
        }
        """
        # Розподіл USDT між лонгом і шортом
        usdt_for_long = free_usdt * (1 - self.hedge_ratio)
        usdt_for_short = free_usdt * self.hedge_ratio

        # Розрахунок qty за цінами виконання
        ask1 = data["ASSET1/USDT"]["ask"]
        bid2 = data["ASSET2/USDT"]["bid"]

        qty_long = usdt_for_long / ask1 if ask1 > 0 else 0
        qty_short = usdt_for_short / bid2 if bid2 > 0 else 0

        signals = []
        if qty_long > 0:
            signals.append({
                "symbol": "ASSET1/USDT",
                "side": "buy",
                "price": ask1,
                "qty": qty_long,
            })
        if qty_short > 0:
            signals.append({
                "symbol": "ASSET2/USDT",
                "side": "sell",
                "price": bid2,
                "qty": qty_short,
            })
        return signals
