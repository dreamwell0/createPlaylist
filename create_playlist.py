import spotipy
import spotipy.util as util
import pandas as pd
import json

 #Spotify APIの認証部分 username, my_id, my_secret は人によって異なる
username = 'XXX' 
my_id ='XXX' 
my_secret = 'XXX' 
redirect_uri = 'http://localhost:8888/callback' 
scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
token = util.prompt_for_user_token(username, scope, my_id, my_secret, redirect_uri)
spotify = spotipy.Spotify(auth = token)

def main():

    playlists = spotify.user_playlist_create(username, '230603New')

    name = 'Radiohead'
    searchResult = spotify.search(q=name, limit=10, offset=0, type='artist', market=None)
    artistId = searchResult['artists']['items'][0]['id']
    print(artistId)
    

    # artist_idからalbumデータを取得
    albumResults = spotify.artist_albums(artistId, limit=50, album_type='album')
    album_datas = albumResults['items']
    while albumResults['next']:
        albumResults = spotify.next(albumResults)
        album_datas.extend(albumResults['items'])
    
    print('全アルバム枚数:', len(album_datas))
    album_sorted = sorted(album_datas, key=lambda x:x['release_date'], reverse=True)

    print(album_sorted[0]['release_date'])

    #tracks_df = AlbumId_To_TrackId(albumid_df) #アルバムIDからトラックIDを取得

    tracks = []
    album_tracks = spotify.album_tracks(album_sorted[0]['id'])

    for track in album_tracks['items']:
        tracks.append(track['id'])
    print(tracks[0])



    results = spotify.user_playlist_add_tracks(username, playlists['id'], [tracks[0]])
    print(results)

if __name__ == "__main__":
    main()
