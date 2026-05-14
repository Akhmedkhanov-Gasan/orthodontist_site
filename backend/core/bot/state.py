from django.conf import settings
from redis import Redis


WAITING_FOR_NAME = "waiting_for_name"
WAITING_FOR_PHONE = "waiting_for_phone"
WAITING_FOR_APPOINTMENT_DATE = "waiting_for_appointment_date"

STATE_TTL_SECONDS = 60 * 30


def get_redis_client():
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_user_state_key(user_id):
    return f"bot:user:{user_id}:state"


def get_registration_name_key(user_id):
    return f"bot:user:{user_id}:registration_name"


def set_user_state(user_id, state):
    redis_client = get_redis_client()
    redis_client.set(get_user_state_key(user_id), state, ex=STATE_TTL_SECONDS)


def get_user_state(user_id):
    redis_client = get_redis_client()
    return redis_client.get(get_user_state_key(user_id))


def clear_user_state(user_id):
    redis_client = get_redis_client()
    redis_client.delete(get_user_state_key(user_id))


def set_registration_name(user_id, name):
    redis_client = get_redis_client()
    redis_client.set(
        get_registration_name_key(user_id),
        name,
        ex=STATE_TTL_SECONDS,
    )


def get_registration_name(user_id):
    redis_client = get_redis_client()
    return redis_client.get(get_registration_name_key(user_id))


def clear_registration(user_id):
    redis_client = get_redis_client()
    redis_client.delete(
        get_user_state_key(user_id),
        get_registration_name_key(user_id),
    )
