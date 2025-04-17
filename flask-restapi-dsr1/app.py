#!usr/bin/env python

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# from datetime import datetime, timedelta
from models import db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Replace with a strong secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = User.hash_password(data["password"])
    new_user = User(username=data["username"], password_hash=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    if not User.verify_password(data["username"], data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.admin})
    return jsonify({"access_token": access_token}), 200


@app.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})


@app.route("/api/test", methods=["GET"])
@jwt_required()
def test():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}! You are authenticated."})


@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(401)
def handle_unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


db.init_app(app)
with app.app_context():
    db.create_all()
