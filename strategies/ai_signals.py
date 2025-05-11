import openai
import json

class AISignals:
    """C9: Генеруємо сигнали через GPT-4 із зрозумілим контролем і виходами."""

    def __init__(self, client, config):
        self.model = config.get("model", "gpt-4")
        self.prompt_template = config.get(
            "prompt_template",
            "Given the market snapshot:\n{snapshot}\n"
            "Generate up to 3 trading signals as a JSON list, "
            "each with symbol, side (buy/sell), price (float), qty (float)."
        )
        openai.api_key = config.get("openai_api_key")

    def generate_signals(self, market_snapshot, free_usdt):
        # Формуємо prompt
        prompt = self.prompt_template.format(snapshot=json.dumps(market_snapshot))
        # Викликаємо GPT
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
        )

        # Парсимо відповідь як JSON
        text = resp.choices[0].message.content
        try:
            signals = json.loads(text)
            # Базова валідація структури
            valid = []
            for s in signals:
                if {"symbol","side","price","qty"} <= s.keys():
                    valid.append({
                        "symbol": s["symbol"],
                        "side": s["side"],
                        "price": float(s["price"]),
                        "qty": float(s["qty"]),
                    })
            return valid
        except Exception:
            # у випадку невдалої відповіді — порожній список
            return []
