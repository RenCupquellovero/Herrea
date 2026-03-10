from flask import Blueprint, render_template, request, redirect, session, send_file
import os
from ..config_loader import load_config
from ..auth import load_user, verify_password
from ..db import get_db

webui_bp = Blueprint("webui", __name__, template_folder="templates", static_folder="static")

config = load_config()

# Load version from root VERSION file
VERSION_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "VERSION")
try:
    with open(VERSION_PATH, "r") as f:
        VERSION = f.read().strip()
except:
    VERSION = "unknown"


# ---------------------------
# ROOT → LOGIN or HOME
# ---------------------------
@webui_bp.route("/")
def root():
    if "user" in session:
        return redirect(config["webui"]["home"])
    return redirect(config["webui"]["login"])


# ---------------------------
# LOGIN
# ---------------------------
@webui_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = load_user(username)
        if user and verify_password(password, user["password"]):
            session["user"] = user
            return redirect(config["webui"]["home"])

        return render_template("login.html",
                               error="Invalid username or password",
                               phrase=config["webui"]["login_phrase"],
                               version=VERSION)

    return render_template("login.html",
                           phrase=config["webui"]["login_phrase"],
                           version=VERSION)


# ---------------------------
# LOGOUT
# ---------------------------
@webui_bp.route("/logout")
def logout():
    session.clear()
    return redirect(config["webui"]["login"])


# ---------------------------
# HOME PAGE
# ---------------------------
@webui_bp.route("/home")
def home():
    if "user" not in session:
        return redirect(config["webui"]["login"])

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM logs WHERE action='add' ORDER BY timestamp DESC LIMIT 5")
    recent_add = cur.fetchall()

    cur.execute("SELECT * FROM logs WHERE action='remove' ORDER BY timestamp DESC LIMIT 5")
    recent_remove = cur.fetchall()

    return render_template("home.html",
                           user=session["user"],
                           recent_add=recent_add,
                           recent_remove=recent_remove,
                           version=VERSION)


# ---------------------------
# STORAGE
# ---------------------------
@webui_bp.route("/items")
def items():
    if "user" not in session:
        return redirect(config["webui"]["login"])

    db = get_db()
    cur = db.cursor()
    team = session["user"]["team"]

    cur.execute("SELECT * FROM items WHERE team=?", (team,))
    rows = cur.fetchall()

    return render_template("items.html", items=rows, version=VERSION)


# ---------------------------
# TODO SECTION
# ---------------------------
@webui_bp.route("/todo")
def todo():
    if "user" not in session:
        return redirect(config["webui"]["login"])

    todos = []  # TODO: implement

    return render_template("todo.html", todos=todos, version=VERSION)


# ---------------------------
# SHARE → PDF
# ---------------------------
@webui_bp.route("/share")
def share():
    if "user" not in session:
        return redirect(config["webui"]["login"])

    return render_template("share.html", version=VERSION)

# ADD ITEM
@webui_bp.route("/items/add", methods=["GET", "POST"])
def items_add():
    if "user" not in session:
        return redirect(config["webui"]["login"])

    if request.method == "POST":
        name = request.form.get("name")
        qty = request.form.get("quantity")
        notes = request.form.get("notes")
        team = session["user"]["team"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO items (name, quantity, notes, team) VALUES (?, ?, ?, ?)",
                    (name, qty, notes, team))
        db.commit()

        return redirect("/items")

    return render_template("items_add.html")
# EDIT ITEM
@webui_bp.route("/items/edit/<int:item_id>", methods=["GET", "POST"])
def items_edit(item_id):
    if "user" not in session:
        return redirect(config["webui"]["login"])

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        qty = request.form.get("quantity")
        notes = request.form.get("notes")

        cur.execute("UPDATE items SET name=?, quantity=?, notes=? WHERE id=?",
                    (name, qty, notes, item_id))
        db.commit()

        return redirect("/items")

    cur.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = cur.fetchone()

    return render_template("items_edit.html", item=item)
# DELETE ITEM
@webui_bp.route("/items/delete/<int:item_id>")
def items_delete(item_id):
    if "user" not in session:
        return redirect(config["webui"]["login"])

    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id=?", (item_id,))
    db.commit()

    return redirect("/items")
