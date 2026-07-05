from fastapi import FastAPI, HTTPException
import redis
import os

app = FastAPI()

# Connect to Redis using the hostname defined in docker-compose.
# decode_responses=True ensures we get strings back instead of bytes.
redis_host = os.environ.get("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.post("/hit/{key}")
def hit_key(key: str):
    # INCR is atomic and creates the key with a value of 1 if it doesn't exist
    count = r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
def get_count(key: str):
    val = r.get(key)
    count = int(val) if val is not None else 0
    return {"key": key, "count": count}

@app.get("/healthz")
def health_check():
    try:
        # Actually ping the Redis server to verify the connection
        if r.ping():
            return {"status": "ok", "redis": "up"}
        else:
            return {"status": "error", "redis": "down"}
    except redis.ConnectionError:
        return {"status": "error", "redis": "down"}
