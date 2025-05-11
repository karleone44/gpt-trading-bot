import openai

class AISignals:
    """C9: Використання GPT для сигналів"""
    def __init__(self, client, config):
        self.model = config.get('model', 'gpt-4')
        self.prompt_template = config.get('prompt_template', '')

    def generate_signals(self, market_snapshot, free_usdt):
        prompt = self.prompt_template.format(snapshot=market_snapshot)
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{'role':'user','content':prompt}]
        )
        # TODO: парсинг відповіді в список сигналів
        return []
