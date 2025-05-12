# strategies/rl_trader.py

import logging
import torch
from stable_baselines3 import PPO

class RLTraderStrategy:
    """
    RL-трейдер на базі Stable-Baselines3 PPO.
    Завантажує збережену модель і генерує сигнали.
    """

    def __init__(self, client, config):
        """
        :param client: ccxt-клієнт біржі
        :param config: dict з config.yaml (env_id, episodes, model_path)
        """
        self.client = client
        self.env_id = config.get('env_id', 'CartPole-v1')
        self.episodes = config.get('episodes', 1000)
        self.model_path = config['model_path']
        # Додамо .zip, тільки якщо його нема
        if not self.model_path.lower().endswith('.zip'):
            self.model_path = f"{self.model_path}.zip"
        self.model = None

    def load(self):
        """Завантажує модель PPO з файлу."""
        try:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model = PPO.load(self.model_path, device=device)
            logging.debug(f"RLTrader: завантажено модель з {self.model_path} на {device}")
        except Exception as e:
            logging.error(f"RLTrader load error: {e}")
            self.model = None

    def generate_signals(self, market_snapshot, free_usdt):
        """
        Генерує сигнали на основі ринкових даних.
        Для прикладу повертає порожній список, якщо моделі немає.
        """
        if self.model is None:
            self.load()
        if self.model is None:
            return []

        # Тут треба перетворити market_snapshot у спостереження (obs)
        # Наприклад:
        # obs = [ ... ]  
        # action, _ = self.model.predict(obs, deterministic=True)
        # return [{"action": action}]  # адаптуйте під ваші потреби

        return []  # заглушка
