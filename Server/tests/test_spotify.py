import pytest
from app.spotify import create_spotify_playlist, add_tracks_to_playlist

# Mock the SpotifyOAuth and Spotify client
@pytest.fixture
def mock_spotify_client(mocker):
    # Patch the 'get_spotify_client' method to return a mock client
    mock_client = mocker.Mock()
    mocker.patch('app.spotify.get_spotify_client', return_value=mock_client)
    return mock_client

def test_create_spotify_playlist(mock_spotify_client):
    # Arrange
    mock_spotify_client.user_playlist_create.return_value = {'id': 'mock_playlist_id'}
    mock_spotify_client.current_user.return_value = {'id': 'mock_user_id'}  # Return a dict from current_user

    # Act
    playlist_id = create_spotify_playlist('Test Playlist')

    # Assert
    assert playlist_id == 'mock_playlist_id'
    mock_spotify_client.user_playlist_create.assert_called_once_with('mock_user_id', 'Test Playlist', public=False)

def test_add_tracks_to_playlist(mock_spotify_client):
    # Arrange
    mock_spotify_client.search.return_value = {'tracks': {'items': [{'uri': 'mock_track_uri'}]}}

    # Act
    success_count = add_tracks_to_playlist('mock_playlist_id', ['Test Track'])

    # Assert
    assert success_count == 1
    mock_spotify_client.playlist_add_items.assert_called_once_with('mock_playlist_id', ['mock_track_uri'])
