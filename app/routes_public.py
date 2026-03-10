from flask import Blueprint, jsonify, request
from .auth import authenticate
from .db import get_db

public_bp = Blueprint("public", __name__)

@public_bp.get("/items")
def get_items():
    user = authenticate(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 403

    team = user.get("team")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE team = ?", (team,))
    rows = cur.fetchall()

    return jsonify({
        "status": "ok",
        "team": team,
        "items": [dict(row) for row in rows]
    })


@public_bp.get("/item/<item_id>")
def get_item(item_id):
    user = authenticate(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 403

    team = user.get("team")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ? AND team = ?", (item_id, team))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "status": "ok",
        "item": dict(row)
    })
