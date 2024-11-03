from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from supabase import create_client, Client

db = SQLAlchemy()

def create_supabase_client():
    supabase_url = Config.SUPABASE_URL
    supabase_key = Config.SUPABASE_KEY
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SUPABASE_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize the SQLAlchemy database with the app

    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Initialize Supabase client
    app.supabase_client = create_supabase_client()

    return app
