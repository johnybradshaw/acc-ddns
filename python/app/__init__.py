from flask import Flask
from dotenv import load_dotenv

def create_app():
    # Load .env file
    load_dotenv()

    app = Flask(__name__)

    # Importing routes
    from .routes import init_app
    init_app(app)

    return app
