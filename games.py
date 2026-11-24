# games.py
# This is our Blueprint. It holds every route that starts with /games
from flask import Blueprint, jsonify, request
from extensions import db
from models import Game

games_bp = Blueprint("games", __name__, url_prefix="/games")

VALID_STATUSES = {"backlog", "playing", "finished"}

def validate_game(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"
    if not partial and "title" not in data:
        return "title is required"
    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return "title must be a non-empty string"
    if "status" in data and data["status"] not in VALID_STATUSES:
        allowed = ", ".join(sorted(VALID_STATUSES))
        return f"status must be one of: {allowed}"
    return None


@games_bp.get("")
def list_games():
    query = Game.query
    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)
    return jsonify([game.to_dict() for game in query.all()])

@games_bp.get("/<int:game_id>")
def get_game(game_id):
    game = db.get_or_404(Game, game_id)
    return jsonify(game.to_dict())

@games_bp.post("")
def create_game():
    data = request.get_json(silent=True)
    error = validate_game(data)
    if error:
        return jsonify({"error": error}), 400

    game = Game(
        title=data["title"].strip(),
        platform=data.get("platform", "PC"),
        status=data.get("status", "backlog"),
    )
    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_dict()), 201

@games_bp.put("/<int:game_id>")
def replace_game(game_id):
    game = db.get_or_404(Game, game_id)

    data = request.get_json(silent=True)
    error = validate_game(data)
    if error:
        return jsonify({"error": error}), 400

    game.title = data["title"].strip()
    game.platform = data.get("platform", "PC")
    game.status = data.get("status", "backlog")
    db.session.commit()
    return jsonify(game.to_dict())

@games_bp.patch("/<int:game_id>")
def update_game(game_id):
    game = db.get_or_404(Game, game_id)

    data = request.get_json(silent=True)
    error = validate_game(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    for field in ("title", "platform", "status"):
        if field in data:
            setattr(game, field, data[field])
    db.session.commit()
    return jsonify(game.to_dict())

@games_bp.delete("/<int:game_id>")
def delete_game(game_id):
    game = db.get_or_404(Game, game_id)
    db.session.delete(game)
    db.session.commit()
    return "", 204