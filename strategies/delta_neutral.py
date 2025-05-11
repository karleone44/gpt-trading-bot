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
        # приклад: довільна логіка delta-neutral
        p1 = (data["ASSET1/USDT"]["bid"] + data["ASSET1/USDT"]["ask"]) / 2
        p2 = (data["ASSET2/USDT"]["bid"] + data["ASSET2/USDT"]["ask"]) / 2

        # розрахунок обсягів
        usdt_for_long = free_usdt * (1 - self.hedge_ratio)
        usdt_for_short = free_usdt * self.hedge_ratio

        qty_long = usdt_for_long / p1 if p1 > 0 else 0
        qty_short = usdt_for_short / p2 if p2 > 0 else 0

        signals = []
        if qty_long > 0:
            signals.append({
                "symbol": "ASSET1/USDT",
                "side": "buy",
                "price": data["ASSET1/USDT"]["ask"],
                "qty": qty_long,
            })
        if qty_short > 0:
            signals.append({
                "symbol": "ASSET2/USDT",
                "side": "sell",
                "price": data["ASSET2/USDT"]["bid"],
                "qty": qty_short,
            })
        return signals
