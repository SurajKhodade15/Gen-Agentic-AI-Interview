import time
from fastapi import HTTPException, Request
from app.services.redis_store import RedisConversationStore

async def enforce_rate_limit(request: Request) -> None:
    """Redis fixed-window limiter; use WAF rate rules as the first perimeter control."""
    identity = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0]
    minute = int(time.time() // 60)
    store = RedisConversationStore().client
    key = f"rate:{identity}:{minute}"
    count = store.incr(key)
    if count == 1:
        store.expire(key, 70)
    if count > 30:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
