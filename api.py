from fastapi import FastAPI
import redis
import json
import os

app = FastAPI()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@app.get("/flips")
def get_flips():
    flips = r.lrange("flips", 0, 20)
    return [eval(f) for f in flips]