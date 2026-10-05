import os
from typing import Optional

import redis
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.tokens import Token

BLACKLIST_PREFIX = "blacklist:"

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


def _make_key(jti: str) -> str:
    return f"{BLACKLIST_PREFIX}{jti}"


def blacklist_access_token(jti: str, ttl: int) -> None:
    redis_client.set(_make_key(jti), "1", ex=ttl)


def is_blacklisted(jti: str) -> bool:
    return redis_client.exists(_make_key(jti)) > 0


class BlackListJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]:
        result = super().authenticate(request)
        if result is None:
            return None
        user, validated_token = result
        jti = validated_token.get('jti')
        if is_blacklisted(jti):
            raise AuthenticationFailed(detail='Token has been revoked')
        return (user, validated_token)