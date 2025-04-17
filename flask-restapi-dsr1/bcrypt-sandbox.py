#!/usr/bin/env python

from flask import Flask
from flask_bcrypt import Bcrypt

# from flask_jwt import JWT, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


def try_brcrypt():
    """learn bcrypt"""
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    msg = "This is my secret message"
    save_msg_hash = bcrypt.generate_password_hash(msg)
    print(f"{save_msg_hash=}")


def try_werkzeug():
    """werkzeug"""
    password = "mysecret"
    hash_pass = generate_password_hash(password)
    print(f"{hash_pass=}")
    if check_password_hash(hash_pass, password):
        print("Success")

    from_next = generate_password_hash(password)
    print(f"{from_next=}")
    if check_password_hash(from_next, password):
        print("Success")


if __name__ == "__main__":
    # try_brcrypt()
    try_werkzeug()
