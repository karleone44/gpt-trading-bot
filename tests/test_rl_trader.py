# tests/test_rl_trader.py

import gym
import pytest
from strategies.rl_trader import RLTrader

@pytest.fixture(autouse=True)
def tmp_model(tmp_path, monkeypatch):
    # Створюємо тимчасовий шлях для моделі та встановлюємо у змінну середовища
    path = tmp_path / "model.zip"
    monkeypatch.setenv("MODEL_PATH", str(path))
    return path

def test_rl_trader_interface(tmp_model):
    # Налаштовуємо конфіг із шляхом до тимчасової моделі
    config = {
        "env_id": "CartPole-v1",
        "episodes": 10,
        "model_path": str(tmp_model),
    }
    trader = RLTrader(None, config)

    # Перед тренуванням модель відсутня
    assert trader.model is None

    # Швидке тренування кілька кроків
    trader.train(env=gym.make("CartPole-v1"))
    assert tmp_model.exists()

    # Завантажуємо натреновану модель
    model = trader.load()
    assert model is not None

    # Генеруємо сигнали, перевіряємо формат
    signals = trader.generate_signals({}, free_usdt=0)
    assert isinstance(signals, list)
    assert "symbol" in signals[0] and "side" in signals[0]
