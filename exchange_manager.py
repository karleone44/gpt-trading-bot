# exchange_manager.py

import os
import ccxt

class ExchangeManager:
    """C12: Менеджер multi-exchange клієнтів (Binance, KuCoin тощо)."""

    def __init__(self, config):
        self.clients = {}
        # Проходимо по всіх біржах із конфігу
        for name in config.get("exchanges", {}):
            key_env = f"{name.upper()}_API_KEY"
            secret_env = f"{name.upper()}_SECRET"
            api_key = os.getenv(key_env)
            secret = os.getenv(secret_env)
            # Якщо є і ключ, і секрет, та ccxt підтримує біржу — створюємо клієнт
            if api_key and secret and hasattr(ccxt, name):
                exchange_cls = getattr(ccxt, name)
                self.clients[name] = exchange_cls({
                    "apiKey": api_key,
                    "secret": secret,
                    "enableRateLimit": True,
                })

    def get(self, name="binance"):
        """Повернути клієнт заданої біржі (за замовчуванням Binance)."""
        return self.clients.get(name)

    def list_exchanges(self):
        """Повернути список доступних бірж."""
        return list(self.clients.keys())
