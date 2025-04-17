from flask import Flask, jsonify, request
# from collections.abc import Mapping

# from werkzeug.exceptions import HTTPException
from flask_bcrypt import Bcrypt
# from flask_jwt import JWT, jwt_required
from flask_jwt_extended import JWTManager, jwt_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Replace with a strong secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


def create_db():
    with app.app_context():
        db.create_all()


create_db()

# JWT configuration
# jwt = JWT(app)
jwt = JWTManager(app)


@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(username=data["username"], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter(User.username == data["username"]).first()
    if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
        token = jwt.encode_jwt({"identity": user.id}, app.config["SECRET_KEY"])
        return jsonify({"token": token.decode("utf-8")}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": f"Protected route accessed by user {current_user.username}"}), 200


if __name__ == "__main__":
    app.run(debug=True)
