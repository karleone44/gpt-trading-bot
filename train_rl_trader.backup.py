#!/usr/bin/env python3
# train_rl_trader.py

import os
import ccxt
import pandas as pd
import numpy as np
import torch as th

import gym
import gym_anytrading
import gym_anytrading.envs
from gym.envs.registration import register
from gym import ObservationWrapper
from gym.spaces import Box

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecEnv
from stable_baselines3.common.callbacks import EvalCallback

# 1) Register custom environment
register(id='Stocks-v0', entry_point='gym_anytrading.envs.stocks_env:StocksEnv')

# 2) Single‐environment Vec wrapper to avoid Shimmy/DummyVecEnv issues
class SingleEnvVec(VecEnv):
    def __init__(self, env):
        super().__init__(num_envs=1, observation_space=env.observation_space, action_space=env.action_space)
        self.env = env
        self._action = None

    def reset(self):
        obs = self.env.reset()
        return np.expand_dims(obs, 0)

    def step_async(self, actions):
        self._action = actions[0]

    def step_wait(self):
        obs, reward, done, info = self.env.step(self._action)
        if done:
            obs = self.env.reset()
        return (
            np.expand_dims(obs, 0),
            np.array([reward], dtype=float),
            np.array([done], dtype=bool),
            [info],
        )

    def close(self):
        self.env.close()

    def render(self):
        return self.env.render()

# 3) Flatten observation wrapper
class FlattenObservation(ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        old = env.observation_space
        low = old.low.flatten()
        high = old.high.flatten()
        self.observation_space = Box(low=low, high=high, dtype=old.dtype)

    def observation(self, obs):
        return obs.flatten()

# 4) Custom features extractor to bypass SB3 preprocessing entirely
class FlatFeaturesExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: Box):
        flat_size = int(np.prod(observation_space.shape))
        super().__init__(observation_space, features_dim=flat_size)

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return observations.view(observations.size(0), -1)

# 5) Data fetcher
def fetch_data(symbol: str, timeframe: str, limit: int = 2000) -> pd.DataFrame:
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['date','open','high','low','close','volume'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)
    df.rename(columns={
        'open':'Open','high':'High','low':'Low',
        'close':'Close','volume':'Volume'
    }, inplace=True)
    return df

# 6) Environment factory
def make_env(df: pd.DataFrame, window_size: int):
    raw = gym.make(
        'Stocks-v0',
        df=df,
        window_size=window_size,
        frame_bound=(window_size, len(df)),
        disable_env_checker=True
    )
    wrapped = FlattenObservation(raw)
    return SingleEnvVec(wrapped)

# 7) Main training loop
def main():
    SYMBOL = 'BTC/USDT'
    TIMEFRAME = '1h'
    WINDOW_SIZE = 50
    TOTAL_TIMESTEPS = 500_000
    MODEL_DIR = 'models'
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("Fetching data...")
    df = fetch_data(SYMBOL, TIMEFRAME)

    print("Preparing training environment...")
    train_env = make_env(df, WINDOW_SIZE)
    print("Preparing evaluation environment...")
    eval_env  = make_env(df, WINDOW_SIZE)

    print("Setting up EvalCallback...")
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=MODEL_DIR,
        log_path=MODEL_DIR,
        eval_freq=50_000,
        deterministic=True,
        render=False
    )

    print("Initializing PPO model with FlatFeaturesExtractor...")
    policy_kwargs = dict(features_extractor_class=FlatFeaturesExtractor)
    model = PPO(
        'MlpPolicy',
        train_env,
        verbose=1,
        policy_kwargs=policy_kwargs,
        device='cpu'
    )

    print(f"Training for {TOTAL_TIMESTEPS} timesteps...")
    model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=eval_callback)

    saved_path = os.path.join(MODEL_DIR, 'rl_trader')
    model.save(saved_path)
    print(f"Training complete! Model saved as {saved_path}.zip")

if __name__ == "__main__":
    main()
