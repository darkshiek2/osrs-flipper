import aiohttp
import asyncio
import redis
import os
from engine import Engine

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
engine = Engine(r)

API_URL = "https://prices.runescape.wiki/api/v1/osrs/5m"

async def run():
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(API_URL) as resp:
                data = await resp.json()
                for item_id, info in data["data"].items():
                    price = info.get("avgHighPrice", 0)
                    volume = info.get("highPriceVolume", 0)
                    history = engine.add_price(item_id, price)
                    limit = 100  # default buy limit
                    result = engine.analyze(item_id, history, volume, limit)
                    if result:
                        r.lpush("flips", str(result))
                        r.ltrim("flips", 0, 50)
            await asyncio.sleep(60)

asyncio.run(run())