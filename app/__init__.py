from flask import Flask
from .config import Config
from supabase import create_client, Client

def create_supabase_client():
    supabase_url = Config.SUPABASE_URL
    supabase_key = Config.SUPABASE_KEY
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Supabase client
    app.supabase_client = create_supabase_client()

    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app