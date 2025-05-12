import json
import logging
import openai

class AISignals:
    def __init__(self, config):
        self.model = config['model']
        openai.api_key = config['openai_api_key']
        self.prompt_template = config['prompt_template']
        logging.debug(f"AISignals initialized with model {self.model}")

    def generate_signals(self, market_snapshot, free_usdt):
        # Serialize snapshot and safely embed into prompt
        try:
            snapshot_json = json.dumps(market_snapshot)
        except (TypeError, ValueError) as e:
            logging.error(f"Failed to serialize market_snapshot: {e}")
            return []
        # Use replace to avoid str.format misinterpreting JSON braces
        prompt = self.prompt_template.replace('{snapshot}', snapshot_json)
        logging.debug(f"AISignals prompt: {prompt}")
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=150,
                n=1,
                temperature=0.7
            )
            text = response['choices'][0]['text']
            logging.debug(f"AISignals raw output: {text}")
            signals = json.loads(text)
            return signals
        except Exception as e:
            logging.error(f"Error generating AI signals: {e}")
            return []
