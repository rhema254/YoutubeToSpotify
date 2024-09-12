from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY')
    YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')
    SPOTIFY_CLIENT_ID = config('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = config('SPOTIFY_CLIENT_SECRET')

class DevConfig(Config):
    REDIRECT_URI = "http://localhost:8888/callback"
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
