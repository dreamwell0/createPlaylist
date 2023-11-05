import spotipy
import spotipy.util as util

class Spotify_token:
    def __init__(self, username):
        self.username = username
        self.scope = 'playlist-modify-public'

    def set(self):
        token = util.prompt_for_user_token(self.username, self.scope)
        return token

# $ vi ~/.bash_profile

# export SPOTIPY_CLIENT_ID='[登録したspotifyアプリのClient ID]'
# export SPOTIPY_CLIENT_SECRET='[登録したspotifyアプリの[Client Secret]'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'