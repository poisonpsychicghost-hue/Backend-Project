import os

class Config():
    DEBUG = False
    JWT_SECRET = os.environ.get("JWT_SECRET")
    INTERNAL_SERVICE_TOKEN = os.environ.get("INTERNAL_SERVICE_TOKEN_SECRET")
    JWT_LIFETIME_HOURS = 2

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    JWT_LIFETIME_HOURS = 4

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    JWT_LIFETIME_HOURS = 4

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    JWT_LIFETIME_HOURS = 2