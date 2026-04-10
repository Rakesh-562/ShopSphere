"""JWT token creation and validation utilities."""
import os
from datetime import datetime, timezone
from functools import wraps

import jwt
import redis
from flask import current_app, g, jsonify, request

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

BLACKLIST_PREFIX = "jwt:blacklist:"


def generate_tokens(user_id: int, email: str, role: str) -> dict:
    now = datetime.now(timezone.utc)
    access_payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
    }
    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"],
    }
    secret = current_app.config["JWT_SECRET_KEY"]
    return {
        "access_token": jwt.encode(access_payload, secret, algorithm="HS256"),
        "refresh_token": jwt.encode(refresh_payload, secret, algorithm="HS256"),
        "token_type": "Bearer",
    }


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config["JWT_SECRET_KEY"],
        algorithms=["HS256"],
    )


def blacklist_token(token: str, expires_in: int) -> None:
    redis_client.setex(f"{BLACKLIST_PREFIX}{token}", expires_in, "revoked")


def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"{BLACKLIST_PREFIX}{token}") == 1


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            if is_token_blacklisted(token):
                return jsonify({"error": "Token has been revoked"}), 401
            payload = decode_token(token)
            if payload.get("type") != "access":
                return jsonify({"error": "Invalid token type"}), 401
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        if g.current_user.get("role") != "ADMIN":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated
