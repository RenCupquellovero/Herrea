from flask import Flask
from .config_loader import load_config
from .routes_public import public_bp
from .routes_admin import admin_bp
from .routes_todos import todos_bp

config = load_config()

def create_app():
    app = Flask(__name__)

    base = config["base_prefix"]
    pub = config["public_api_prefix"]
    adm = config["admin_api_prefix"]

    app.register_blueprint(public_bp, url_prefix=base + pub)
    app.register_blueprint(admin_bp, url_prefix=base + adm)
    app.register_blueprint(todos_bp, url_prefix=base + adm)

    return app