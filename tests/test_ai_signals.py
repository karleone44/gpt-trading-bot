import json
import pytest
from unittest.mock import patch
from strategies.ai_signals import AISignals

@pytest.fixture
def fake_snapshot():
    return {
        "BTC/USDT": {"bid": 50000.0, "ask": 50100.0},
        "ETH/USDT": {"bid": 4000.0, "ask": 4050.0}
    }

def test_ai_signals_parsing_valid_json(fake_snapshot):
    dummy_choice = {
        "choices": [{
            "message": {
                "content": json.dumps([
                    {"symbol": "BTC/USDT", "side": "buy", "price": 50100.0, "qty": 0.01},
                    {"symbol": "ETH/USDT", "side": "sell", "price": 4000.0, "qty": 0.1}
                ])
            }
        }]
    }
    with patch("openai.ChatCompletion.create", return_value=dummy_choice):
        ai = AISignals(
            client=None,
            config={
                "model": "gpt-4",
                "openai_api_key": "testkey",
                "prompt_template": "{snapshot}"
            }
        )
        signals = ai.generate_signals(fake_snapshot, free_usdt=1000)
        assert isinstance(signals, list)
        assert signals[0] == {
            "symbol": "BTC/USDT", "side": "buy",
            "price": 50100.0, "qty": 0.01
        }
        assert signals[1]["symbol"] == "ETH/USDT"
        assert signals[1]["side"] == "sell"

def test_ai_signals_handles_invalid_json(fake_snapshot):
    bad_response = {"choices": [{"message": {"content": "not a json"}}]}
    with patch("openai.ChatCompletion.create", return_value=bad_response):
        ai = AISignals(
            client=None,
            config={
                "model": "gpt-4",
                "openai_api_key": "testkey",
                "prompt_template": "{snapshot}"
            }
        )
        signals = ai.generate_signals(fake_snapshot, free_usdt=1000)
        assert signals == []
