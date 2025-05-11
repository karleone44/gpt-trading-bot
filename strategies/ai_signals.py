# strategies/ai_signals.py

import openai
import json

class AISignals:
    """C9: Генеруємо сигнали через GPT-4 із підтримкою фейкових dict у тестах."""

    def __init__(self, client, config):
        self.client = client
        self.model = config.get("model", "gpt-4")
        self.prompt_template = config.get(
            "prompt_template",
            "Given the market snapshot:\n{snapshot}\nGenerate up to 3 trading signals as JSON list."
        )
        api_key = config.get("openai_api_key")
        if api_key:
            openai.api_key = api_key

    def generate_signals(self, market_snapshot, free_usdt):
        # Формуємо prompt
        prompt = self.prompt_template.format(snapshot=json.dumps(market_snapshot))

        # Викликаємо GPT
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
        )

        # Підтримуємо і dict, і OpenAIObject
        if isinstance(response, dict):
            choices = response.get("choices", [])
        else:
            choices = getattr(response, "choices", [])

        if not choices:
            return []

        first_choice = choices[0]

        # Витягаємо content
        if isinstance(first_choice, dict):
            message = first_choice.get("message", {})
            text = message.get("content", "")
        else:
            text = first_choice.message.content

        # Парсимо JSON
        try:
            raw = json.loads(text)
            signals = []
            for s in raw:
                if {"symbol", "side", "price", "qty"} <= set(s.keys()):
                    signals.append({
                        "symbol": s["symbol"],
                        "side": s["side"],
                        "price": float(s["price"]),
                        "qty": float(s["qty"]),
                    })
            return signals
        except Exception:
            return []
