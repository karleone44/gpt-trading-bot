from strategies.tri_arb import TriArbStrategy


def test_tri_arb_no_profit():
    strat = TriArbStrategy(
        None,
        {
            "pairs": ["BTC/USDT", "ETH/USDT", "ETH/BTC"],
            "usdt_pct": 0.1,
            "min_profit": 1,  # достатньо високий, щоб не було профіту
            "commission": 0.001,
        },
    )
    data = {
        "BTC/USDT": {"ask": 100},
        "ETH/BTC": {"ask": 0.05},
        "ETH/USDT": {"bid": 5},
    }
    # При таких параметрах profit<min_profit => ніяких сигналів
    signals = strat.generate_signals(data, free_usdt=1000)
    assert signals == []
