from flask import Blueprint, request, jsonify
from .auth import authenticate, check_privilege
from .db import get_db

admin_bp = Blueprint("admin", __name__)

@admin_bp.post("/add")
def add_item():
    user = authenticate(request)
    if not user or not check_privilege(user, "readwrite"):
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json() or {}
    name = data.get("name")
    quantity = data.get("quantity", 0)
    team = data.get("team")
    notes = data.get("notes")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO items (name, quantity, team, notes) VALUES (?, ?, ?, ?)",
        (name, quantity, team, notes)
    )
    item_id = cur.lastrowid

    cur.execute(
        "INSERT INTO logs (action, item_id, username) VALUES (?, ?, ?)",
        ("add", item_id, user.get("username"))
    )

    db.commit()

    return jsonify({"status": "added", "id": item_id})


@admin_bp.post("/remove")
def remove_item():
    user = authenticate(request)
    if not user or not check_privilege(user, "readwrite"):
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json() or {}
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "missing id"}), 400

    db = get_db()
    cur = db.cursor()

    # delete item
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))

    # log action
    cur.execute(
        "INSERT INTO logs (action, item_id, username) VALUES (?, ?, ?)",
        ("remove", item_id, user.get("username"))
    )

    db.commit()

    return jsonify({"status": "removed"})


@admin_bp.post("/edit")
def edit_item():
    user = authenticate(request)
    if not user or not check_privilege(user, "readwrite"):
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json() or {}
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "missing id"}), 400

    fields = []
    values = []

    for key in ("name", "quantity", "team", "notes"):
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])

    if not fields:
        return jsonify({"error": "no fields to update"}), 400

    values.append(item_id)

    db = get_db()
    cur = db.cursor()
    cur.execute(f"UPDATE items SET {', '.join(fields)} WHERE id = ?", values)
    cur.execute(
        "INSERT INTO logs (action, item_id, username) VALUES (?, ?, ?)",
        ("edit", item_id, user.get("username"))
    )
    db.commit()

    return jsonify({"status": "edited"})


@admin_bp.get("/logs")
def get_logs():
    user = authenticate(request)
    if not user or not check_privilege(user, "readonly"):
        return jsonify({"error": "unauthorized"}), 403

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    rows = cur.fetchall()

    return jsonify({
        "status": "ok",
        "logs": [dict(row) for row in rows]
    })
