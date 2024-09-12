from googleapiclient.discovery import build
from flask import current_app


def get_youtube_playlist(playlist_id):
    # 1. Create the Youtube Api Client

    youtube = build('youtube', 'v3', developerKey=current_app.config['YOUTUBE_API_KEY'])

    # 2. Fetching Playlist Items

    tracks = []
    next_page_token = None

    while True:
        playlist_items = youtube.playlistItems().list(
            part = 'snippet',
            playlist_id = playlist_id,
            maxResults = 50,
            pageToken = next_page_token
        ).execute()

        for item in playlist_items['items']:
            video_title = item['snippet']['title']
            tracks.append(video_title)

        next_page_token = playlist_items.get('nextPageToken')
        if not next_page_token:
            break

    return tracks



        