# strategies/rl_trader.py

import gym
import torch
from stable_baselines3 import PPO

class RLTrader:
    """C10: Reinforcement Learning Agent (PPO) skeleton."""

    def __init__(self, client, config):
        self.client = client
        self.env_id = config.get("env_id", "CartPole-v1")
        self.episodes = config.get("episodes", 1000)
        self.model_path = config.get("model_path", "rl_trader.zip")
        self.model = None

    def train(self, env=None):
        """Train the agent in the specified gym environment."""
        env = env or gym.make(self.env_id)
        self.model = PPO("MlpPolicy", env, verbose=0)
        self.model.learn(total_timesteps=self.episodes)
        self.model.save(self.model_path)

    def load(self):
        """Load a pre-trained model from disk."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = PPO.load(self.model_path, device=device)
        return self.model

    def generate_signals(self, market_snapshot, free_usdt):
        """
        Generate trading signals based on the agent's action.
        If prediction fails (e.g., bad observation), fall back to a default action.
        """
        if self.model is None:
            self.load()

        try:
            obs = self._prepare_observation(market_snapshot, free_usdt)
            action, _ = self.model.predict(obs, deterministic=True)
        except Exception:
            # Fallback to 'buy' if anything in prediction goes wrong
            action = 0

        # Simple mapping: action 0 = buy, else sell
        if action == 0:
            return [{"symbol": "BTC/USDT", "side": "buy", "price": None, "qty": None}]
        return [{"symbol": "BTC/USDT", "side": "sell", "price": None, "qty": None}]

    def _prepare_observation(self, market_snapshot, free_usdt):
        """
        Convert market_snapshot and free_usdt into model observation.
        TODO: implement proper normalization/formatting.
        """
        # Placeholder: return raw snapshot; model.predict will be wrapped above
        return market_snapshot
