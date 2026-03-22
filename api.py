# api.py
from fastapi import FastAPI
import os

app = FastAPI(title="OSRS Flipper Dashboard")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Example endpoint to show current flipping status
@app.get("/status")
def flipping_status():
    # Replace with your real logic or DB connection
    example_status = {
        "bot_running": True,
        "active_flips": 3,
        "last_alert": "Dragon bones dumped"
    }
    return example_status

if __name__ == "__main__":
    import uvicorn
    # Get port from Fly.io environment variable
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("api:app", host="0.0.0.0", port=port)