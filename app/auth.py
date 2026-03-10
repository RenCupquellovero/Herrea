import os
import json
import bcrypt
from .config_loader import load_config

config = load_config()
USERS_DIR = config["users_dir"]

def load_user(username):
    path = os.path.join(USERS_DIR, f"{username}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def verify_password(raw, hashed):
    return bcrypt.checkpw(raw.encode(), hashed.encode())

def check_privilege(user, required):
    priv = user.get("privilege", "readonly")
    if priv == "readwrite":
        return True
    if priv == "readonly" and required == "readonly":
        return True
    return False

def authenticate(request):
    header_user = config["auth"]["header_user"]
    header_pass = config["auth"]["header_pass"]

    username = request.headers.get(header_user)
    password = request.headers.get(header_pass)

    if not username or not password:
        return None

    user = load_user(username)
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user
