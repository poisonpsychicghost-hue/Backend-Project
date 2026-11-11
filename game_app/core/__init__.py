import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate
from .blueprints.base import base_game_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()
    from .config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
    app.config["APP_ENV"] = os.environ.get("APP_ENV")
    if app.config["APP_ENV"] == "testing":
        app.config.from_object(TestingConfig)
    elif app.config["APP_ENV"] == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    


    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(base_game_bp)
    print(f'DATABASE: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    return app


