from flask import Flask, request, redirect, session, url_for, render_template
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials


app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
#Youtube Details
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
YOUTUBE_PROJECT_ID = os.getenv('YOUTUBE_PROJECT_ID')
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Create a mock client_secrets.json structure
CLIENT_SECRETS = {
    "web": {
        "client_id": YOUTUBE_CLIENT_ID,
        "project_id": YOUTUBE_PROJECT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "redirect_uris": [
            "http://localhost:5000/youtube_callback"
        ]
    }
}


@app.route('/youtube_auth')
def youtube_auth():
    flow = Flow.from_client_config(
        client_config=CLIENT_SECRETS,
        scopes=YOUTUBE_SCOPES
    )
    flow.redirect_uri = url_for('youtube_callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['youtube_state'] = state
    return redirect(authorization_url)

@app.route('/youtube_callback')
def youtube_callback():
    flow = Flow.from_client_config(
        client_config=CLIENT_SECRETS,
        scopes=YOUTUBE_SCOPES,
        state=session['youtube_stafte']
    )
    flow.redirect_uri = url_for('youtube_callback', _external=True)
    
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['youtube_credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('spotify_auth'))

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


if __name__  == "__main__":
    app.run(debug=True)

# def youtube_authentication():
#     """ This will do:
#     1. Fetch the youtube token
#     2. Return the token """
#     pass

# def get_spotify_oauth():
#     return SpotifyOAuth(
#         client_id=SPOTIFY_CLIENT_ID,
#         client_secret=SPOTIFY_CLIENT_SECRET,
#         redirect_uri=SPOTIFY_REDIRECT_URI,
#         scope='playlist-modify-private'
#     )


# def convert_YouTube_to_Spotify():
#     """ This will do multiple things:
#       1. 
#       2. Fetch the youtube playlist
#       3. Return the list of Songs """
#     pass


# def create_spotify_playlist():
#     """ This will do:
#     1. Fetch the List of songs from the create_Youtube_to_Spotify fn.
#     2. Search for each song in the List
#     3. Create a private/public playlist
#     4. Add the songs to the playlist
#     5. Return the spotify playlist link """
#     pass
