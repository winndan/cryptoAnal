import asyncio
from get_realtime import AlpacaWebSocket

async def main():
    alpaca_ws = AlpacaWebSocket()
    await asyncio.gather(alpaca_ws.connect(), alpaca_ws.save_to_json())

if __name__ == "__main__":
    asyncio.run(main())
