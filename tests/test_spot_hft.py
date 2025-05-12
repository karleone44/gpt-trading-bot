from strategies.spot_hft import SpotHFT


def test_spot_hft_buy_and_sell():
    strat = SpotHFT(None, {"spread_threshold": 0.01})

    # Якщо спред ≤ threshold → buy
    buy_signals = strat.generate_signals({"bid": 100, "ask": 100.5})
    assert len(buy_signals) == 1
    assert buy_signals[0]["side"] == "buy"
    assert buy_signals[0]["price"] == 100.5

    # Якщо спред ≥ threshold → sell
    sell_signals = strat.generate_signals({"bid": 99, "ask": 100})
    assert len(sell_signals) == 1
    assert sell_signals[0]["side"] == "sell"
    assert sell_signals[0]["price"] == 99
