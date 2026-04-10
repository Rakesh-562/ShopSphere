"""
Auth routes: /api/v1/auth
POST /register  — create account
POST /login     — get JWT tokens
POST /refresh   — refresh access token
POST /logout    — revoke token (blacklist)
POST /validate  — internal endpoint for gateway token check
"""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.db.database import db
from app.models.user import User
from app.schema.auth_schema import LoginSchema, RegisterSchema
from app.core.security import generate_tokens, decode_token, blacklist_token, jwt_required
import jwt
import logging

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.post("/register")
def register():
    """Register a new user."""
    try:
        data = register_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    tokens = generate_tokens(user.id, user.email, user.role.value)
    logger.info(f"New user registered: {user.email}")
    return jsonify({"user": user.to_dict(), **tokens}), 201


@auth_bp.post("/login")
def login():
    """Authenticate user and return JWT tokens."""
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    tokens = generate_tokens(user.id, user.email, user.role.value)
    logger.info(f"User logged in: {user.email}")
    return jsonify({"user": user.to_dict(), **tokens}), 200


@auth_bp.post("/refresh")
def refresh():
    """Issue a new access token using a valid refresh token."""
    data = request.get_json() or {}
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "refresh_token is required"}), 400

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            return jsonify({"error": "Invalid token type"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401

    user = User.query.get(int(payload["sub"]))
    if not user or not user.is_active:
        return jsonify({"error": "User not found or inactive"}), 401

    tokens = generate_tokens(user.id, user.email, user.role.value)
    return jsonify(tokens), 200


@auth_bp.post("/logout")
@jwt_required
def logout():
    """Blacklist the current access token."""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ", 1)[1]
    payload = decode_token(token)
    exp = payload["exp"]
    import time
    ttl = max(int(exp - time.time()), 1)
    blacklist_token(token, ttl)
    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.post("/validate")
def validate_token():
    """
    Internal endpoint called by API Gateway to validate JWT.
    Returns user claims if valid.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"valid": False, "error": "Missing token"}), 401
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        return jsonify({
            "valid": True,
            "user_id": payload["sub"],
            "email": payload["email"],
            "role": payload["role"],
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401
