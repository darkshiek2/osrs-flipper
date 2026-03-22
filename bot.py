import discord
import redis
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    last_seen = set()
    while True:
        flips = r.lrange("flips", 0, 10)
        for f in flips:
            if f in last_seen:
                continue
            last_seen.add(f)
            data = eval(f)
            msg = (
                f"💰 **FLIP ALERT**\n"
                f"Item: {data['item_id']}\n"
                f"Profit: {int(data['profit']):,} GP\n"
                f"Score: {data['score']:.2f}"
            )
            await channel.send(msg)
        await asyncio.sleep(30)

client.run(TOKEN)