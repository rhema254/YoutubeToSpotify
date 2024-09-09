from flask import Flask
import json
import requests
# from flask_restx import Resource, Api,


app = Flask(__name__)

def youtube_authentication():
    """ This will do:
    1. Fetch the youtube token
    2. Return the token """
    pass

def spotify_authentication():
    """ This will do:
    1. Fetch the spotify token
    2. Return the token """
    pass


def convert_YouTube_to_Spotify():
    """ This will do multiple things:
      1. 
      2. Fetch the youtube playlist
      3. Return the list of Songs """
    pass


def create_spotify_playlist():
    """ This will do:
    1. Fetch the List of songs from the create_Youtube_to_Spotify fn.
    2. Search for each song in the List
    3. Create a private/public playlist
    4. Add the songs to the playlist
    5. Return the spotify playlist link """
    pass



if __name__  == "__main__":
    app.run(debug=True)