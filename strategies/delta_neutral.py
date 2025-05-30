# strategies/delta_neutral.py

import logging

class DeltaNeutralStrategy:
    """
    Простий дельта-нейтральний алгоритм:
    порівнює ask першого актива і bid другого,
    генерує сигнал продажу першого та купівлі другого.
    """

    def __init__(self, client, config):
        self.client = client
        self.window = config['window']
        self.hedge_ratio = config['hedge_ratio']
        asset1 = config.get('asset1')
        asset2 = config.get('asset2')

        if 'symbols' in config:
            self.symbols = config['symbols']
        elif asset1 and asset2:
            self.symbols = [asset1, asset2]
        else:
            # Значення за замовчуванням для тестів
            self.symbols = ['ASSET1/USDT', 'ASSET2/USDT']

    def generate_signals(self, market_snapshot, free_usdt):
        """Generate hedged buy/sell signals based on snapshot data."""
        try:
            sym1, sym2 = self.symbols
            data1 = market_snapshot.get(sym1)
            data2 = market_snapshot.get(sym2)
            if data1 is None or data2 is None:
                logging.error(f"Missing data for {sym1} or {sym2}")
                return []

            ask1 = float(data1["ask"])
            bid2 = float(data2["bid"])

            ratio = ask1 / bid2
            threshold = 1 + (1 - self.hedge_ratio)

            if ratio > threshold and free_usdt > 0:
                # Розподіляємо available USDT згідно з hedge_ratio
                amount1 = free_usdt * (1 - self.hedge_ratio)
                amount2 = free_usdt * self.hedge_ratio
                qty1 = amount1 / ask1
                qty2 = amount2 / bid2

                return [
                    {
                        "side": "sell",
                        "symbol": sym1,
                        "price": ask1,
                        "qty": qty1,
                    },
                    {
                        "side": "buy",
                        "symbol": sym2,
                        "price": bid2,
                        "qty": qty2,
                    },
                ]
            return []
        except Exception as e:
            logging.error(f"DeltaNeutralStrategy error: {e}")
            return []

