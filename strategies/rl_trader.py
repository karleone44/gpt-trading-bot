class RLTrader:
    """C10: Reinforcement Learning Agent skeleton"""
    def __init__(self, client, config):
        self.client = client
        self.episodes = config.get('episodes', 1000)

    def train(self, historical_data):
        # TODO: навчання агента на historical_data
        pass

    def generate_signals(self, market_snapshot, free_usdt):
        # TODO: використання натренованого агента
        return []
