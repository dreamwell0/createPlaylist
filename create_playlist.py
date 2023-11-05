# create_playlist.py
# Creates a playlist for a user

import sys
import pprint
import spotipy
from spotify_token import Spotify_token

# usage
# $ python create_playlist.py [username] [playlist_name]
username = sys.argv[1]
playlist_name = sys.argv[2]

ST = Spotify_token(username)
token = ST.set()

sp = spotipy.Spotify(auth=token)
sp.trace = False
playlists = sp.user_playlist_create(username, playlist_name)
pprint.pprint(playlists)

