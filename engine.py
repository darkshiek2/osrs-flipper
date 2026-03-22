import json
from collections import deque
from ml import compute_features, score_flip

HISTORY_LENGTH = 4

class Engine:
    def __init__(self, redis_client):
        self.redis = redis_client

    def add_price(self, item_id, price):
        key = f"history:{item_id}"
        history = self.redis.get(key)
        if history:
            history = deque(json.loads(history), maxlen=HISTORY_LENGTH)
        else:
            history = deque(maxlen=HISTORY_LENGTH)
        history.append(price)
        self.redis.set(key, json.dumps(list(history)))
        return history

    def analyze(self, item_id, history, volume, limit):
        if len(history) < HISTORY_LENGTH:
            return None
        features = compute_features(history, volume, limit)
        if features["drop"] < 0.05 or features["margin"] < 0.03:
            return None
        score = score_flip(features)
        buy = history[-2]
        sell = history[-1]
        profit_each = (sell - buy) * 0.99
        total_profit = profit_each * limit
        if total_profit < 10_000_000:
            return None
        return {
            "item_id": item_id,
            "buy": buy,
            "sell": sell,
            "profit": total_profit,
            "score": score,
            **features
        }