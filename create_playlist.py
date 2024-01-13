import spotipy
import spotipy.util as util
import json
import os

#Spotify APIの認証部分 username, my_id, my_secret は人によって異なる
username = '' 
my_id ='' 
my_secret = '' 
redirect_uri = 'http://localhost:8888/callback' 
scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'
token = util.prompt_for_user_token(username, scope, my_id, my_secret, redirect_uri)
spotify = spotipy.Spotify(auth = token)

def main():

    dir_path = 'data/'
    files = os.listdir(dir_path)  # ディレクトリ内のファイルリストを取得
    files.sort(reverse=True)  # ファイルリストを降順に並び替え
    idx = files[0].find('.')
    playlistname = files[0][:idx] + 'New'
    playlists = spotify.user_playlist_create(username, playlistname)

    f = open(dir_path + files[0], 'r')
    datalist = f.readlines()

    for name in datalist:
        if name == '\n':
            continue
        # 括弧より前までをArtist名とする
        idx = name.find('(')
        name = name[:idx]

        search_result = spotify.search(q=name, limit=10, offset=0, type='artist', market=None)
        artist_Id = search_result['artists']['items'][0]['id']
        
        # artist_idからalbumデータを取得
        album_results = spotify.artist_albums(artist_Id, limit=50, album_type='album')
        album_datas = album_results['items']
        while album_results['next']:
            album_results = spotify.next(album_results)
            album_datas.extend(album_results['items'])
        
        # 発売日の降順にソート
        album_sorted = sorted(album_datas, key=lambda x:x['release_date'], reverse=True)

        # album_idからalbumのtrackデータを取得
        tracks = []
        album_tracks = spotify.album_tracks(album_sorted[0]['id'])

        for track in album_tracks['items']:
            tracks.append(track['id'])

        # trackデータの1曲目,2曲目をプレイリストに追加
        results = spotify.user_playlist_add_tracks(username, playlists['id'], [tracks[0],tracks[1]])

    f.close()

if __name__ == "__main__":
    main()
