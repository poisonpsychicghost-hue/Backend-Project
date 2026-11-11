from flask import Blueprint, jsonify


base_game_bp = Blueprint("roman-province", __name__, url_prefix="/")

def load_game():
    print("Loading Game Called")
    return "Loading Game..."

def route_health_check():
    print("Health Route Called")
    return jsonify({"status": "ok"}), 200

base_game_bp.add_url_rule(
    "/loading",
    view_func=load_game,
    methods=["GET"]
)

base_game_bp.add_url_rule(
    "/health",
    view_func=route_health_check,
    methods=["GET"]
)
