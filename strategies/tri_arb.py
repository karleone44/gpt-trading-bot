# strategies/tri_arb.py

class TriArbStrategy:
    def __init__(self, client, config):
        self.client = client
        # Три символи для арбітражу, наприклад ['BTC/USDT','ETH/USDT','ETH/BTC']
        self.pairs = config.get('pairs', ['BTC/USDT', 'ETH/USDT', 'ETH/BTC'])
        # Частка вільного USDT для арбітражу
        self.usdt_pct = config.get('usdt_pct', 0.01)

    def generate_signals(self, data, free_usdt):
        """
        data: dict з ticker’ами для self.pairs, кожен має 'bid' і 'ask'
        free_usdt: float
        """
        signals = []
        # Простий приклад: купуємо BTC за USDT, потім ETH за BTC, потім продаємо ETH за USDT
        # Оцінюємо, чи є profit > 0
        # Крок 1: USDT -> BTC
        btc_amount = (free_usdt * self.usdt_pct) / data['BTC/USDT']['ask']
        # Крок 2: BTC -> ETH
        eth_amount = btc_amount / data['ETH/BTC']['ask']
        # Крок 3: ETH -> USDT
        final_usdt = eth_amount * data['ETH/USDT']['bid']
        profit = final_usdt - (free_usdt * self.usdt_pct)
        if profit > 0:
            # Подаємо сигнали по трьох ордерах
            signals.append({'symbol': 'BTC/USDT', 'side': 'buy',  'qty': btc_amount, 'price': data['BTC/USDT']['ask']})
            signals.append({'symbol': 'ETH/BTC', 'side': 'buy',  'qty': eth_amount, 'price': data['ETH/BTC']['ask']})
            signals.append({'symbol': 'ETH/USDT', 'side': 'sell', 'qty': eth_amount, 'price': data['ETH/USDT']['bid']})
        return signals
