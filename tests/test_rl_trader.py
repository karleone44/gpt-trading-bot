import os
import gym
from strategies.rl_trader import RLTrader

def test_rl_trader_smoke(tmp_path, monkeypatch):
    # Тестовий шлях для збереження моделі
    model_file = tmp_path / "model.zip"
    config = {
        "env_id": "CartPole-v1",
        "episodes": 10,
        "model_path": str(model_file),
    }
    trader = RLTrader(None, config)

    # Без тренування модель None
    assert trader.model is None

    # Навчаємо кілька кроків
    trader.train(env=gym.make("CartPole-v1"))
    assert model_file.exists()

    # Завантажуємо модель
    model = trader.load()
    assert model is not None

    # Генеруємо хоча б один сигнал
    sigs = trader.generate_signals({}, free_usdt=0)
    assert isinstance(sigs, list) and "symbol" in sigs[0]
