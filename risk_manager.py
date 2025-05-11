# risk_manager.py

class RiskManager:
    def __init__(self, config):
        self.max_drawdown_pct = config.get('risk.max_drawdown_pct', 0.05)
        self.daily_loss_limit = config.get('risk.daily_loss_limit', 0.02)
        self.start_balance = None
        self.daily_loss = 0.0

    def initialize(self, total_balance):
        """
        Викликається на старті сесії, щоб зафіксувати початковий баланс.
        """
        self.start_balance = total_balance.get('USDT', 0)
        self.daily_loss = 0.0

    def update_daily_loss(self, pnl):
        """
        Оновлюємо накопичений збиток за день.
        pnл < 0 додає збиток.
        """
        if pnl < 0:
            self.daily_loss += abs(pnl)

    def filter_signals(self, signals, balance):
        """
        Фільтруємо сигнали за правилами:
        - Не перевищувати max_drawdown_pct від стартового балансу
        - Не перевищувати daily_loss_limit
        balance: словник total балансу
        """
        if self.start_balance is None:
            self.initialize(balance)
        total_usdt = balance.get('USDT', 0)
        drawdown = (self.start_balance - total_usdt) / self.start_balance
        if drawdown >= self.max_drawdown_pct:
            print(f"RiskManager: досягнуто max_drawdown_pct ({drawdown:.2%}), блокування угод.")
            return []
        if self.daily_loss / self.start_balance >= self.daily_loss_limit:
            print("RiskManager: досягнуто daily_loss_limit, блокування угод.")
            return []
        return signals
