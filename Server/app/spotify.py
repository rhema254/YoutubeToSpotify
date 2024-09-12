import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import current_app

# Function to get the spotify client
def get_spotify_client():
    return spotipy.Spotify( auth_manager=SpotifyOAuth(
        client_id = current_app.config["SPOTIFY_CLIENT_ID"],
        client_secret = current_app.config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri = current_app.config["REDIRECT_URI"],
        scope = "playlist-modify-private"
    ))

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