from redis import Redis
from django.contrib.auth.models import User

def get_user_key(User):
    return f"{User.username}:{User.id}"

def get_redis_instance():
    return Redis(host='redis', port=6379, db=0)