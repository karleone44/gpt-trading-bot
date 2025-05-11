import ccxt

class ExchangeManager:
    """C12: Менеджер для багатьох бірж"""
    def __init__(self, configs):
        # configs: { 'binance': {...}, 'kucoin': {...}, ... }
        self.exchanges = {
            name: getattr(ccxt, name)(cfg)
            for name, cfg in configs.items()
        }

    def fetch_all_tickers(self):
        data = {}
        for name, ex in self.exchanges.items():
            data[name] = ex.fetch_tickers()
        return data
