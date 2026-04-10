"""
User profile routes: /api/v1/users
GET  /me          — get own profile
PUT  /me          — update own profile
PUT  /me/password — change password
GET  /            — list users (admin only)
"""
from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError
from app.db.database import db
from app.models.user import User
from app.schema.auth_schema import ChangePasswordSchema, UpdateProfileSchema
from app.core.security import jwt_required, admin_required

user_bp = Blueprint("users", __name__)

update_schema = UpdateProfileSchema()
pwd_schema = ChangePasswordSchema()


@user_bp.get("/me")
@jwt_required
def get_profile():
    user = User.query.get_or_404(int(g.current_user["sub"]))
    return jsonify(user.to_dict()), 200


@user_bp.put("/me")
@jwt_required
def update_profile():
    try:
        data = update_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    user = User.query.get_or_404(int(g.current_user["sub"]))
    for field, value in data.items():
        setattr(user, field, value)
    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.put("/me/password")
@jwt_required
def change_password():
    try:
        data = pwd_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    user = User.query.get_or_404(int(g.current_user["sub"]))
    if not user.check_password(data["current_password"]):
        return jsonify({"error": "Current password is incorrect"}), 400

    user.set_password(data["new_password"])
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200


@user_bp.get("/")
@admin_required
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = User.query.order_by(User.id).paginate(page=page, per_page=per_page)
    return jsonify({
        "items": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    }), 200
