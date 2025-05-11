from strategies.grid import GridStrategy


def test_grid_levels_and_qty_pct():
    # Ініціалізуємо стратегію з двома рівнями і qty_pct
    strat = GridStrategy(None, {"levels": [-0.01, 0.02], "qty_pct": 0.1})
    data = {"bid": 100, "ask": 102}
    signals = strat.generate_signals(data)

    # Має бути два сигнали
    assert len(signals) == 2

    # Перевіряємо ціну buy і sell
    buy_price = signals[0]["price"]
    sell_price = signals[1]["price"]
    mid = (100 + 102) / 2

    assert round(buy_price, 4) == round(mid * 0.99, 4)
    assert round(sell_price, 4) == round(mid * 1.02, 4)

    # Кількість через qty_pct — не None
    assert "qty_pct" in signals[0] and signals[0]["qty_pct"] == 0.1
