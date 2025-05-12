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
        self.symbols = config.get('symbols', ['BTC/USDT', 'ETH/USDT'])

    def generate_signals(self, market_snapshot, free_usdt):
        try:
            sym1, sym2 = self.symbols
            data1 = market_snapshot.get(sym1)
            data2 = market_snapshot.get(sym2)
            if data1 is None or data2 is None:
                logging.error(f"Missing data for {sym1} or {sym2}")
                return []

            ask1 = float(data1['ask'])
            bid2 = float(data2['bid'])
            ratio = ask1 / bid2

            if ratio > 1 + (1 - self.hedge_ratio):
                return [
                    {"side": "sell", "symbol": sym1, "price": ask1},
                    {"side": "buy",  "symbol": sym2, "price": bid2}
                ]
            return []
        except Exception as e:
            logging.error(f"DeltaNeutralStrategy error: {e}")
            return []

