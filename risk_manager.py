class RiskManager:
    """Фільтрація сигналів за дроудауном та лімітом втрат."""

    def __init__(self, config):
        self.max_dd = config.get("risk.max_drawdown_pct", 0.05)
        self.daily_loss_limit = config.get("risk.daily_loss_limit", 0.02)
        self.start_balance = None
        self.daily_loss = 0.0

    def initialize(self, balance):
        """Встановлює стартовий баланс."""
        self.start_balance = balance.get("USDT", 0)
        self.daily_loss = 0.0

    def filter_signals(self, signals, balance):
        """Блокує сигнали при перевищенні ризик-лімітів."""
        if self.start_balance is None:
            self.initialize(balance)

        current = balance.get("USDT", 0)
        drawdown = (self.start_balance - current) / self.start_balance

        if drawdown >= self.max_dd:
            print(f"DD ≥ {self.max_dd * 100:.1f}% — трейди заблоковано")
            return []

        if self.daily_loss / self.start_balance >= self.daily_loss_limit:
            print("Daily loss limit досягнуто — трейди заблоковано")
            return []

        return signals
