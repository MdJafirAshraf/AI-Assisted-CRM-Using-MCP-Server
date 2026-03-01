import hashlib
from app.chatbot.cache_service import redis_client

CACHE_TTL = 60 * 60  # 1 hour


def generate_cache_key(user_id: str, query: str) -> str:
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    return f"chat:{user_id}:{query_hash}"


def get_cached_response(user_id: str, query: str):
    key = generate_cache_key(user_id, query)
    return redis_client.get(key)


def set_cached_response(user_id: str, query: str, response: str):
    key = generate_cache_key(user_id, query)
    redis_client.setex(key, CACHE_TTL, response)