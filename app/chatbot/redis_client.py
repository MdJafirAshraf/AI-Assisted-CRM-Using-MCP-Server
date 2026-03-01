import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)

def get_user_data_version(user_id: str) -> str:
    version = redis_client.get(f"crm:data_version:{user_id}")
    return version or "1"


def bump_user_data_version(user_id: str):
    redis_client.incr(f"crm:data_version:{user_id}")


if __name__ == "__main__":
    # Test connection
    try:
        redis_client.ping()
        print("Connected to Redis successfully!")
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")