from flask import Flask
from .config_loader import load_config
from .routes_public import public_bp
from .routes_admin import admin_bp
from .webui.routes_webui import webui_bp   # ← ADD THIS

config = load_config()

def create_app():
    app = Flask(__name__)
    app.secret_key = "CHANGE_ME"  # required for sessions

    base = config["base_prefix"]
    pub = config["public_api_prefix"]
    adm = config["admin_api_prefix"]

    # API
    app.register_blueprint(public_bp, url_prefix=base + pub)
    app.register_blueprint(admin_bp, url_prefix=base + adm)

    # WEBUI
    app.register_blueprint(webui_bp, url_prefix=config["webui"]["root"])

    return app
