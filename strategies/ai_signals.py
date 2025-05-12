import json
import logging
from openai import OpenAI

class AISignals:
    def __init__(self, config):
        # Беремо ключ із конфига або середовища, якщо він у форматі ${…}
        key = config['openai_api_key']
        if isinstance(key, str) and key.startswith('${') and key.endswith('}'):
            import os
            key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key)

        self.model  = config['model']
        self.prompt_template = config['prompt_template']

    def generate_signals(self, market_snapshot, free_usdt):
        prompt = self.prompt_template.replace(
            '{snapshot}', json.dumps(market_snapshot)
        )
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            logging.error(f"AI Signals error: {e}")
            return []
