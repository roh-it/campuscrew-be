from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Initialize the database with the app

    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
