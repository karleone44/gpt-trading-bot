# execution_module.py

import ccxt

def execute_orders(client, signals):
    """
    Виконує список сигналів. Якщо лімітний ордер не проходить
    через фільтри Binance, робимо маркет-ордер.
    Кожен сигнал – словник з keys:
      - 'symbol' (str), наприклад 'BTC/USDT'
      - 'side' ('buy' або 'sell')
      - 'price' (float) – для лімітного ордера, або None
      - 'qty' (float) – кількість базової валюти
    """
    for sig in signals:
        symbol = sig.get('symbol', 'BTC/USDT')
        side   = sig['side']
        price  = sig.get('price')
        qty    = sig.get('qty')
        if not qty or qty <= 0:
            continue
        try:
            if price:
                # пробуємо лімітний ордер
                order = client.create_order(symbol, 'limit', side, qty, price)
                print(f"ExecutionModule: limit order placed: {side} {qty:.6f} {symbol} at {price} ⇒ {order}")
            else:
                # якщо price=None або ліміт не вказаний, робимо маркет
                order = client.create_order(symbol, 'market', side, qty)
                print(f"ExecutionModule: market order placed: {side} {qty:.6f} {symbol} ⇒ {order}")
        except ccxt.BadRequest as e:
            # фільтр не дав лімітному ордеру — робимо маркет
            print(f"ExecutionModule: limit order failed ({e}), placing market order instead")
            try:
                order = client.create_order(symbol, 'market', side, qty)
                print(f"ExecutionModule: market order placed: {side} {qty:.6f} {symbol} ⇒ {order}")
            except Exception as e2:
                print(f"ExecutionModule: market order also failed: {e2}")
        except Exception as e:
            print(f"ExecutionModule: unexpected error for {symbol} {side} {qty} @ {price}: {e}")
