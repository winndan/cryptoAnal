import asyncio
import websockets
import json
import os
import pandas as pd
from dotenv import load_dotenv

class AlpacaWebSocket:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("alpaca_key")
        self.secret_key = os.getenv("alpaca_secret")
        self.ws_url = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"
        self.output_file = "alpaca_data.json"
        self.df = pd.DataFrame(columns=["timestamp", "symbol", "price", "size", "event"])

    async def save_to_json(self):
        """Continuously save only the latest record to JSON."""
        while True:
            try:
                if not self.df.empty:
                    latest_record = self.df.iloc[-1:].to_dict(orient="records")
                    with open(self.output_file, "w") as f:
                        json.dump(latest_record, f, indent=4)
                    print(f"✅ Overwritten data in {self.output_file}")
            except Exception as e:
                print(f"❌ Error saving to JSON: {e}")
            await asyncio.sleep(5)

    async def connect(self):
        """Connect to Alpaca WebSocket and stream latest data only."""
        while True:
            try:
                async with websockets.connect(self.ws_url, ping_interval=30) as ws:
                    print("🔗 Connected to Alpaca WebSocket.")

                    # Authenticate
                    auth_payload = {"action": "auth", "key": self.api_key, "secret": self.secret_key}
                    await ws.send(json.dumps(auth_payload))
                    auth_response = json.loads(await ws.recv())
                    print("🔑 Auth Response:", auth_response)

                    if not any(resp.get("T") == "success" for resp in auth_response):
                        print("❌ Authentication failed. Check API credentials.")
                        return

                    # Subscribe to data
                    subscribe_payload = {
                        "action": "subscribe",
                        "trades": ["DOGE/USD", "ETH/USD"],
                        "quotes": ["DOGE/USD"],
                        "bars": ["DOGE/USD"]
                    }
                    await ws.send(json.dumps(subscribe_payload))

                    while True:
                        try:
                            data = await ws.recv()
                            data_json = json.loads(data)

                            for event in data_json:
                                if not isinstance(event, dict) or "T" not in event:
                                    print(f"⚠️ Unexpected message format: {event}")
                                    continue

                                event_map = {
                                    "t": {"key": "p", "event": "trade"},
                                    "q": {"key": "bp", "event": "quote"},
                                    "b": {"key": "c", "event": "bar"}
                                }

                                event_type = event["T"]
                                if event_type in event_map:
                                    new_data = {
                                        "timestamp": event.get("t"),
                                        "symbol": event.get("S"),
                                        "price": event.get(event_map[event_type]["key"]),
                                        "size": event.get("s", event.get("bs", event.get("v"))),
                                        "event": event_map[event_type]["event"]
                                    }
                                    if None not in new_data.values():
                                        self.df = pd.DataFrame([new_data])
                                        print(f"📈 Updated {event_map[event_type]['event'].capitalize()}: {new_data}")
                                    else:
                                        print(f"⚠️ Missing data: {event}")
                        except websockets.exceptions.ConnectionClosed:
                            print("⚠️ Connection lost. Reconnecting in 5 seconds...")
                            await asyncio.sleep(5)
                            break
            except Exception as e:
                print(f"❌ WebSocket Error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

async def main():
    """Run WebSocket connection and JSON saver concurrently."""
    alpaca_ws = AlpacaWebSocket()
    await asyncio.gather(alpaca_ws.connect(), alpaca_ws.save_to_json())

if __name__ == "__main__":
    asyncio.run(main())
