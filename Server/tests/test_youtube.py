import pytest
from unittest.mock import patch, MagicMock
from app.youtube import get_youtube_playlist
from app import create_app
from config import DevConfig

# Mock YouTube API Response
mocked_playlist_response = {
    'items': [
        {'snippet': {'title': 'Track 1'}},
        {'snippet': {'title': 'Track 2'}}
    ],
    'nextPageToken': None
}

@pytest.fixture
def app():
    # Create a test app and set up the context
    app = create_app(DevConfig)  # Ensure 'testing' is a valid config or adjust as needed
    with app.app_context():
        yield app

@patch('app.youtube.build')  # Mock the build function from googleapiclient.discovery
def test_get_youtube_playlist(mock_build, app):
    # Create a mock YouTube client and set up the mock API response
    mock_youtube = MagicMock()
    mock_list = MagicMock()
    mock_execute = MagicMock()
    
    # Set up the mock for playlistItems().list().execute
    mock_list.execute.return_value = mocked_playlist_response
    mock_youtube.playlistItems.return_value.list.return_value = mock_list
    
    mock_build.return_value = mock_youtube

    # Call the function
    playlist_id = 'fake_playlist_id'
    tracks = get_youtube_playlist(playlist_id)

    # Assert that the function returned the correct number of tracks
    assert len(tracks) == 2
    assert tracks == ['Track 1', 'Track 2']

    # Check if the YouTube API was called with the correct parameters
    mock_youtube.playlistItems().list.assert_called_with(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=None
    )

    # Check if execute() was called once
    mock_list.execute.assert_called_once()
