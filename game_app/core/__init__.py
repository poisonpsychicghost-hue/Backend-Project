from flask import Flask
#from dotenv import load_dotenv
from .extensions import db, migrate
from .blueprints.base import base_game_bp

def create_app():
    app = Flask(__name__)
    #load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(base_game_bp)

    return app


