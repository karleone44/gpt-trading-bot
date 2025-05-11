# exchange_manager.py

import os
import ccxt

class ExchangeManager:
    """C12: Менеджер multi-exchange клієнтів (Binance, KuCoin тощо)."""

    def __init__(self, config):
        self.clients = {}
        exch_cfg = config.get("exchanges", {})

        # Binance
        bin_cfg = exch_cfg.get("binance", {})
        if bin_cfg.get("api_key") and bin_cfg.get("secret"):
            self.clients["binance"] = ccxt.binance({
                "apiKey": os.getenv("BINANCE_API_KEY"),
                "secret": os.getenv("BINANCE_SECRET"),
                "enableRateLimit": True,
            })

        # KuCoin
        ku_cfg = exch_cfg.get("kucoin", {})
        if ku_cfg.get("api_key") and ku_cfg.get("secret"):
            self.clients["kucoin"] = ccxt.kucoin({
                "apiKey": os.getenv("KUCOIN_API_KEY"),
                "secret": os.getenv("KUCOIN_SECRET"),
                "enableRateLimit": True,
            })

    def get(self, name="binance"):
        """Повернути клієнт заданої біржі (за замовчуванням Binance)."""
        return self.clients.get(name)

    def list_exchanges(self):
        """Повернути список доступних бірж."""
        return list(self.clients.keys())
