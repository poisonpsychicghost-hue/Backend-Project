from flask import Blueprint

base_game_bp = Blueprint("roman-province", __name__, url_prefix="/")

def load_game():
    print("Loading Game Called")
    return "Loading Game..."

base_game_bp.add_url_rule(
    "/loading",
    view_func=load_game,
    methods=["GET"]
)