import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import current_app, session, redirect, request, url_for

def get_spotify_oauth():
    """Creates a SpotifyOAuth object with the required configuration."""
    return SpotifyOAuth(
        client_id=current_app.config["SPOTIFY_CLIENT_ID"],
        client_secret=current_app.config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=current_app.config["REDIRECT_URI"],
        scope=current_app.config["SCOPES"]
    )

# Spotify Login Route
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Spotify Callback Route
def callback():
    sp_oauth = get_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    # Store token info in the session
    session['token_info'] = token_info
    return redirect(url_for('index'))

def ensure_token():
    """Checks and refreshes the Spotify token if necessary."""
    sp_oauth = get_spotify_oauth()
    token_info = session.get('token_info')

    # If token info is not in session, redirect to login
    if not token_info:
        return redirect(url_for('login'))
    
    # Refresh the token if it is expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info  # Update session with new token

    return token_info['access_token']

def get_spotify_client():
    """Returns a Spotify client with an ensured access token."""
    access_token = ensure_token()
    return spotipy.Spotify(auth=access_token)

def create_spotify_playlist(name):
    sp = get_spotify_client()
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, name, public=False)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_names):
    sp = get_spotify_client()
    success_count = 0
    for track_name in track_names:
        results = sp.search(q=track_name, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.playlist_add_items(playlist_id, [track_uri])
            success_count += 1
    return success_count

def add_single_song_to_spotify_playlist(playlist_id, song_name):
    """Search for a song on Spotify and add it to the specified playlist."""
    sp = get_spotify_client()  # Get authenticated Spotify client
    results = sp.search(q=song_name, type='track', limit=1)  # Search for the song
    
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id, [track_uri])
        return True
    return False