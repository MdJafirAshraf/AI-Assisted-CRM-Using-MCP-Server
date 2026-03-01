import inspect
from functools import wraps
from app.chatbot.redis_client import bump_user_data_version

def invalidate_user_cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        # Handle both async and sync functions
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        current_user = kwargs.get("current_user")

        if current_user:
            bump_user_data_version(str(current_user.id))

        return result

    return wrapper