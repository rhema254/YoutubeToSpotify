from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask import current_app, redirect, request, session, url_for, flash
import random
import string
import json

# Scope needed to access private playlists
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Generate a random string for the state parameter
def generate_state():
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return state

def youtube_login():
    """Initiate the OAuth login process for YouTube."""
    state = generate_state()  # Generate the state
    session['oauth_state'] = state  # Store it in the session

    flow = Flow.from_client_secrets_file(
        current_app.config['YOUTUBE_OAUTH_CLIENT_SECRETS_FILE'],
        scopes=SCOPES,
        redirect_uri=current_app.config['REDIRECT_URI']
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', state=state)
    return redirect(auth_url)

def youtube_callback():
    """Handle the callback from YouTube OAuth and obtain credentials."""
    # Retrieve the state parameter from the session
    stored_state = session.get('oauth_state')
    returned_state = request.args.get('state')

    if stored_state != returned_state:
        flash("State mismatch. Potential CSRF attack detected.")
        return "Error: State did not match. Please try again or contact support."

    flow = Flow.from_client_secrets_file(
        current_app.config['YOUTUBE_OAUTH_CLIENT_SECRETS_FILE'],
        scopes=SCOPES,
        redirect_uri=current_app.config['REDIRECT_URI']
    )
    
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        session['youtube_credentials'] = credentials.to_json()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred during the authentication process: {str(e)}")
        return "Error: Failed to fetch token. Please try again or contact support."

def get_youtube_service():
    """Authenticate and return the YouTube API client with session credentials."""
    if 'youtube_credentials' in session:
        credentials_info = json.loads(session['youtube_credentials'])
        credentials = Credentials.from_authorized_user_info(credentials_info, SCOPES)

        # Check if token is expired and refresh if necessary
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                session['youtube_credentials'] = credentials.to_json()
            except Exception as e:
                flash(f"Error refreshing credentials: {str(e)}")
                return redirect(url_for('youtube_login'))

        youtube = build('youtube', 'v3', credentials=credentials)
        return youtube
    else:
        # Redirect to login if credentials are missing
        return redirect(url_for('youtube_login'))

def is_playlist_public(playlist_id):
    """Check if the playlist is public using YouTube API key."""
    try:
        youtube = build('youtube', 'v3', developerKey=current_app.config['YOUTUBE_API_KEY'])
        playlist = youtube.playlists().list(
            part='status',
            id=playlist_id
        ).execute()

        # If the playlist exists and is found, check the status
        if playlist['items']:
            return playlist['items'][0]['status']['privacyStatus'] == 'public'
    except Exception as e:
        flash(f"Error checking playlist privacy: {str(e)}")
    
    return False

def get_youtube_playlist(playlist_id, is_authenticated=False):
    """Fetch the playlist from YouTube (public or private)."""
    try:
        # If the playlist is public, no need for OAuth
        if not is_authenticated and is_playlist_public(playlist_id):
            youtube = build('youtube', 'v3', developerKey=current_app.config['YOUTUBE_API_KEY'])
        else:
            # If playlist is private or user is authenticated, use OAuth
            youtube = get_youtube_service()
            if not youtube:
                return "Redirecting to login..."

        tracks = []
        next_page_token = None

        while True:
            playlist_items = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_items['items']:
                tracks.append(item['snippet']['title'])

            next_page_token = playlist_items.get('nextPageToken')
            if not next_page_token:
                break

        return tracks
    except Exception as e:
        flash(f"Error fetching playlist: {str(e)}")
        return []

def get_youtube_song(song_id):
    """Fetch a single song from YouTube based on the song ID."""
    youtube = get_youtube_service()  # Get authenticated YouTube API client
    video = youtube.videos().list(part='snippet', id=song_id).execute()
    
    # Return the title of the song
    return video['items'][0]['snippet']['title']