# execution_module.py

def execute_orders(client, signals, symbol="BTC/USDT"):
    balance = client.fetch_balance()
    free_usdt = balance.get('free', {}).get('USDT', 0)
    if free_usdt <= 0:
        print("ExecutionModule: немає вільного USDT для торгівлі.")
        return
    for sig in signals:
        side = sig['side']
        price = sig['price']
        qty_pct = sig.get('qty_pct', 0.01)
        amount_usdt = free_usdt * qty_pct
        qty = amount_usdt / price if price > 0 else 0
        order = client.create_order(symbol, 'limit', side, qty, price)
        print(f"ExecutionModule: placed {side} {qty:.6f} at {price} => {order}")
