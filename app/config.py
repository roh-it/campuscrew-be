import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    DB_USER = 'user1' or 'username'
    DB_PASSWORD = 'campuscr3W.' or 'password'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_NAME = "campuscrew"

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
