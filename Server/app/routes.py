from flask import Blueprint, request, jsonify, render_template
from app.youtube import get_youtube_playlist
from app.spotify import create_spotify_playlist, add_tracks_to_playlist


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('Landing.html')

@bp.route('/convert', methods=['POST'])
def convert_playlist():
    data = request.json
    youtube_playlist_id = data.get('youtube_playlist_id')
    spotify_playlist_name = data.get('spotify_playlist_name')

#Remove in case of any errors><
    if not youtube_playlist_id or not spotify_playlist_name:
        return jsonify({'error': 'Missing required fields'}), 400

    #Get all the Youtube tracks in playlist
    youtube_tracks = get_youtube_playlist(youtube_playlist_id)

    #Create Spotify Playlist
    spotify_playlist_id = create_spotify_playlist(spotify_playlist_name)

    #success
    success_count = add_tracks_to_playlist(spotify_playlist_id, youtube_tracks)

    return jsonify({ 'message': f'Converted {success_count} out of {len(youtube_tracks)} tracks',
        'spotify_playlist_id': spotify_playlist_id})