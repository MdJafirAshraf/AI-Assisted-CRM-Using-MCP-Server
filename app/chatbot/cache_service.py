import re, hashlib
from app.chatbot.redis_client import redis_client, get_user_data_version

CACHE_TTL = 60 * 60  # 1 hour

def normalize_query(query: str) -> str:
    query = query.lower().strip()
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r"[^\w\s]", "", query)
    return query


def generate_cache_key(user_id: str, query: str) -> str:
    normalized = normalize_query(query)
    query_hash = hashlib.sha256(normalized.encode()).hexdigest()
    version = get_user_data_version(user_id)

    return f"crm:chat:{user_id}:{version}:{query_hash}"


def get_cached_response(user_id: str, query: str):
    key = generate_cache_key(user_id, query)
    return redis_client.get(key)


def set_cached_response(user_id: str, query: str, response: str):
    key = generate_cache_key(user_id, query)
    redis_client.setex(key, CACHE_TTL, response)