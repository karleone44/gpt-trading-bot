from strategies.auto_invest import AutoInvest


def test_auto_invest_basic():
    symbols = ["BTC/USDT", "ETH/USDT"]
    ai = AutoInvest(None, {"symbols": symbols, "qty_pct": 0.1})
    # Дані: ціни
    data = {"BTC/USDT": {"price": 100}, "ETH/USDT": {"price": 50}}
    free_usdt = 1000
    signals = ai.generate_signals(data, free_usdt)
    # Має бути по 2 сигнали: купівля BTC та ETH
    assert len(signals) == 2
    # Перевіримо qty = free_usdt*qty_pct/price
    btc_qty = signals[0]["qty"]
    eth_qty = signals[1]["qty"]
    assert round(btc_qty, 6) == round((1000 * 0.1) / 100, 6)
    assert round(eth_qty, 6) == round((1000 * 0.1) / 50, 6)
