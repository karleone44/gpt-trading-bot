# tests/test_rl_trader.py

import gym
import numpy as np
import pytest
from strategies.rl_trader import RLTrader

# Додаємо numpy.bool8 для сумісності з Gym/stable-baselines3
np.bool8 = np.bool_

@pytest.fixture(autouse=True)
def tmp_model(tmp_path, monkeypatch):
    # Створюємо тимчасовий файл моделі
    path = tmp_path / "model.zip"
    monkeypatch.setenv("MODEL_PATH", str(path))
    return path

def test_rl_trader_interface(tmp_model):
    config = {
        "env_id": "CartPole-v1",
        "episodes": 10,
        "model_path": str(tmp_model),
    }
    trader = RLTrader(None, config)

    # Спочатку модель має бути None
    assert trader.model is None

    # Швидке тренування — лише 10 кроків
    trader.train(env=gym.make("CartPole-v1"))
    assert tmp_model.exists()

    # Завантаження моделі
    model = trader.load()
    assert model is not None

    # Генерація сигналів
    signals = trader.generate_signals({}, free_usdt=0)
    assert isinstance(signals, list)
    assert "symbol" in signals[0] and "side" in signals[0]
