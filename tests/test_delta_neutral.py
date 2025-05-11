from strategies.delta_neutral import DeltaNeutralStrategy


def test_delta_neutral_basic():
    # setup
    config = {"window": 60, "hedge_ratio": 0.3}
    strat = DeltaNeutralStrategy(None, config)
    data = {
        "ASSET1/USDT": {"bid": 10, "ask": 11},
        "ASSET2/USDT": {"bid": 5, "ask": 5.5},
    }
    free_usdt = 1000

    signals = strat.generate_signals(data, free_usdt)

    # повинно вийти два сигнали
    assert len(signals) == 2

    # перевіряємо суму USDT, що розподілили на лонг/шорт
    total_qty1 = signals[0]["qty"] * 11
    total_qty2 = signals[1]["qty"] * 5
    # приблизно: 0.7*1000 на лонг, 0.3*1000 на шорт
    assert round(total_qty1, 1) == round(free_usdt * 0.7, 1)
    assert round(total_qty2, 1) == round(free_usdt * 0.3, 1)
