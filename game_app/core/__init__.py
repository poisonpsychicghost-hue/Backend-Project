from flask import Flask
from dotenv import load_dotenv

def create_app(config_name):
    app = Flask(__name__)
    load_dotenv()

