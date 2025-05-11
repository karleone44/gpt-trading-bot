# ws_connector.py

import asyncio
import json
import websockets

class WSConnector:
    """
    Простий WebSocket-клієнт для підписки на потоки Binance (або інші).
    Використовує callbacks для обробки отриманих даних.
    """
    def __init__(self, url):
        self.url = url
        self.handlers = {}

    def subscribe(self, stream: str, callback):
        """
        stream: рядок виду "btcusdt@trade"
        callback: функція, яка приймає декодований JSON `data`
        """
        self.handlers[stream] = callback

    async def run(self):
        async with websockets.connect(self.url) as ws:
            # Підписуємося на всі стріми
            for stream in self.handlers:
                sub = {
                    "method": "SUBSCRIBE",
                    "params": [stream],
                    "id": 1
                }
                await ws.send(json.dumps(sub))

            # Читаємо повідомлення безкінечно
            while True:
                raw = await ws.recv()
                msg = json.loads(raw)
                stream = msg.get("stream")
                data = msg.get("data")
                if stream in self.handlers and data is not None:
                    self.handlers[stream](data)
