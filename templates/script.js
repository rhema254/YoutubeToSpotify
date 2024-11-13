// Global state variables
let youtubePlaylists = [];  // Store playlists from YouTube
let selectedPlaylist = null;

// Step 1: Select Source
document.getElementById('youtube').addEventListener('click', function() {
    document.getElementById('step2').style.display = 'block';
});

// Step 2: Enter URL or Load from YouTube Account
document.getElementById('load_from_youtube').addEventListener('click', function() {
    // Call backend to fetch the user’s YouTube playlists (this part needs backend API)
    fetch('/youtube/playlists')  // Assuming this endpoint exists and returns user playlists
        .then(response => response.json())
        .then(data => {
            youtubePlaylists = data.playlists;
            updatePlaylistSelect();  // Update the UI with available playlists
        })
        .catch(error => alert('Error loading YouTube playlists'));
});

document.getElementById('playlist_url').addEventListener('change', function(e) {
    // Parse playlist or song URL and show options accordingly
    const url = e.target.value;
    if (url) {
        // This should parse the URL and get the playlist or song ID
        console.log('Playlist/Song URL:', url);
    }
});

// Step 3: Select Playlist/Song to Move
function updatePlaylistSelect() {
    const selectDiv = document.getElementById('playlist_select');
    selectDiv.innerHTML = ''; // Clear existing options

    youtubePlaylists.forEach(playlist => {
        const button = document.createElement('button');
        button.textContent = playlist.name;
        button.addEventListener('click', function() {
            selectedPlaylist = playlist;
            updateSummary();
        });
        selectDiv.appendChild(button);
    });
}

// Step 4: Select Destination
document.getElementById('spotify_dest').addEventListener('click', function() {
    document.getElementById('step5').style.display = 'block';
    document.getElementById('step4').style.display = 'none';
});

// Step 5: Summary
function updateSummary() {
    const summaryText = document.getElementById('summary');
    if (selectedPlaylist) {
        summaryText.textContent = `You selected the playlist: ${selectedPlaylist.name}`;
    }
}

// Step 6: Start Transfer
document.getElementById('start_transfer').addEventListener('click', function() {
    // Call the backend to start the conversion process
    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            youtube_playlist_id: selectedPlaylist.id,
            spotify_playlist_name: 'New Spotify Playlist'
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Show success message
    })
    .catch(error => alert('Error during transfer'));
});
