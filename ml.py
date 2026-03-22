import numpy as np

def compute_features(history, volume, limit):
    prices = np.array(history)
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)
    drop = (prices[0] - prices[-2]) / prices[0]
    rebound = (prices[-1] - prices[-2]) / prices[-2]
    margin = (prices[-1] - prices[-2]) / prices[-2]
    momentum = np.mean(returns)
    return {
        "drop": drop,
        "rebound": rebound,
        "volume": volume,
        "volatility": volatility,
        "margin": margin,
        "limit": limit,
        "momentum": momentum
    }

def score_flip(f):
    score = (
        f["drop"] * 2.0 +
        f["rebound"] * 2.5 +
        f["margin"] * 3.0 +
        f["volatility"] * 1.5 +
        (f["volume"] / 100000) +
        (f["limit"] / 1000) +
        f["momentum"] * 2.0
    )
    return score