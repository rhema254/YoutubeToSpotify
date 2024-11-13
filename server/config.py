import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

class DevConfig(Config):
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
    REDIRECT_URI = os.getenv('REDIRECT_URI')  # Use a production redirect URI if applicable
