# tests/test_exchange_manager.py

import os
import pytest
from exchange_manager import ExchangeManager

@pytest.fixture(autouse=True)
def fake_env(monkeypatch):
    # Підміняємо змінні середовища для API ключів
    monkeypatch.setenv("BINANCE_API_KEY", "key1")
    monkeypatch.setenv("BINANCE_SECRET", "sec1")
    monkeypatch.setenv("KUCOIN_API_KEY", "key2")
    monkeypatch.setenv("KUCOIN_SECRET", "sec2")

def test_exchange_manager_listing_and_clients():
    cfg = {
        "exchanges": {
            "binance": {},
            "kucoin": {},
        }
    }
    mgr = ExchangeManager(cfg)
    exs = mgr.list_exchanges()
    assert set(exs) == {"binance", "kucoin"}

    bin_client = mgr.get("binance")
    ku_client  = mgr.get("kucoin")
    # Клієнти повинні підтримувати fetch_balance()
    assert callable(getattr(bin_client, "fetch_balance"))
    assert callable(getattr(ku_client, "fetch_balance"))
