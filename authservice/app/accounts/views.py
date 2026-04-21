from flask import Blueprint,flash,redirect,render_template,request,url_for,jsonify
from flask_login import login_user,logout_user,login_required,current_user
from app import db,bcrypt
from app.accounts.models import User
from .form import RegisterForm,LoginForm
from flask_jwt_extended import create_access_token

accounts_bp = Blueprint("accounts", __name__)
@accounts_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400


    # Create user
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201
@accounts_bp.route("/login")
def login():
    return redirect("http://localhost:5173/login")


@accounts_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401

@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect("http://localhost:5173/login")
