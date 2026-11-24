import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate
from .blueprints.base import base_game_bp
from .user.user_routes import user_route_bp
from .user.admin_routes import admin_route_bp
from .province.province_routes import province_route_bp
from .errors import bad_request_handler, unauthorized_handler, forbidden_handler, not_found_handler, not_allowed_handler, service_error_handler

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
    
    from . import user
    from . import province

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(base_game_bp)
    app.register_blueprint(user_route_bp)
    app.register_blueprint(admin_route_bp)
    app.register_blueprint(province_route_bp)
    app.register_error_handler(400, bad_request_handler)
    app.register_error_handler(401, unauthorized_handler)
    app.register_error_handler(403, forbidden_handler)
    app.register_error_handler(404, not_found_handler)
    app.register_error_handler(405, not_allowed_handler)
    app.register_error_handler(500, service_error_handler)
    print(f'DATABASE: {app.config["SQLALCHEMY_DATABASE_URI"]}')

    return app

