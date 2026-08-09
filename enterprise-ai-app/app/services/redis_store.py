import json
from redis import Redis
from app.core.config import get_settings

class RedisConversationStore:
    """Shared, TTL-bound chat memory for horizontally scaled ECS tasks."""
    def __init__(self) -> None:
        self.cfg = get_settings()
        self.client = Redis.from_url(self.cfg.redis_url, decode_responses=True)

    def append(self, tenant_id: str, conversation_id: str, role: str, content: str) -> None:
        key = f"chat:{tenant_id}:{conversation_id}"
        self.client.rpush(key, json.dumps({"role": role, "content": content}))
        self.client.expire(key, self.cfg.redis_ttl_seconds)

    def history(self, tenant_id: str, conversation_id: str) -> list[dict]:
        return [json.loads(item) for item in self.client.lrange(f"chat:{tenant_id}:{conversation_id}", 0, -1)]

    def healthy(self) -> bool:
        return bool(self.client.ping())
