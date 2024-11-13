import os
from flask import Flask, redirect, request, session, jsonify, url_for
from spotipy.oauth2 import SpotifyOAuth
from spotify import login, callback, create_spotify_playlist, add_tracks_to_playlist, add_single_song_to_spotify_playlist
from youtube import get_youtube_playlist, get_youtube_song
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)  # Load from config file

@app.route('/spotify/login')
def login():
    return login()

@app.route('/spotify/callback')
def callback():
    return callback()

# Route to handle the playlist conversion (also works for single songs)
@app.route('/convert', methods=['POST'])
def convert_playlist():
    data = request.json
    youtube_playlist_id = data.get('youtube_playlist_id')  # Playlist ID from YouTube
    youtube_song_id = data.get('youtube_song_id')  # Single song ID from YouTube
    spotify_playlist_name = data.get('spotify_playlist_name')

    # Check for missing fields
    if not spotify_playlist_name or (not youtube_playlist_id and not youtube_song_id):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new Spotify playlist
    spotify_playlist_id = create_spotify_playlist(spotify_playlist_name)

    success_count = 0

    # Handle YouTube playlist to Spotify playlist conversion
    if youtube_playlist_id:
        youtube_tracks = get_youtube_playlist(youtube_playlist_id)
        success_count = add_tracks_to_playlist(spotify_playlist_id, youtube_tracks)  # Adding multiple tracks

    # Handle single song ID to Spotify playlist conversion
    if youtube_song_id:
        song_title = get_youtube_song(youtube_song_id)  # Fetch the song title from YouTube
        if add_single_song_to_spotify_playlist(spotify_playlist_id, song_title):  # Adding single song to Spotify
            success_count += 1

    return jsonify({
        'message': f'Converted {success_count} tracks.',
        'spotify_playlist_id': spotify_playlist_id
    })

# Index Route (Landing page)
@app.route('/')
def index():
    return "Welcome to the Spotify to YouTube Playlist Converter!"

if __name__ == '__main__':
    app.run(debug=True)
