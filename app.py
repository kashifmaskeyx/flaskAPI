from flask import Flask, jsonify
from config import Config
from extensions import db
from games import games_bp
from errors import register_error_handlers
from models import Game

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(games_bp)
    register_error_handlers(app)


    @app.route("/")
    def home():
        return jsonify({"name": "Game Backlog API", "version": "1.0"})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

   
    @app.cli.command("seed")
    def seed():
        db.session.add_all([
            Game(title="Hollow Knight", platform="PC", status="playing"),
            Game(title="Celeste", platform="Switch", status="finished"),
            Game(title="Elden Ring", platform="PS5", status="backlog"),
        ])
        db.session.commit()
        print("Seeded 3 games")

    
    with app.app_context():
        db.create_all()

    return app