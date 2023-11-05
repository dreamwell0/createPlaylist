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

# .pyファイルがあるフォルダに221221.txt
# (サイトから取ってきたIDをコピペしたtxtファイル)があり，読み込ませている
date = "221221" 

def main():
    data = Read_Dataset(date) #サイトから取ってきたリストをdataframeに変換
    albumid_df = Dataset_To_AlbumId(data) #アルバムIDを取得
    tracks_df = AlbumId_To_TrackId(albumid_df) #アルバムIDからトラックIDを取得
    make_playlist(tracks_df) #プレイリスト作成

def Read_Dataset(str): 
    df = pd.read_csv(str + ".txt",encoding="utf_8",header=None)
    return df

def Get_AlbumId(str):
    str = str.replace('spotify:track:','')
    df_track = spotify.track(str)
    dict_album = df_track['album']['external_urls']
    str_albumid = json.dumps(dict_album)
    str_albumid = str_albumid.replace('{\"spotify\": \"https://open.spotify.com/album/','')
    str_albumid = str_albumid.replace('\"}','')
    return str_albumid

def Dataset_To_AlbumId(dataframe) :
    return dataframe.applymap(Get_AlbumId)

def Get_TrackId_From_Tracks(dict):
    dict_url = dict["external_urls"]
    str_url = json.dumps(dict_url)
    str_url = str_url.replace('{\"spotify\": "','')
    str_url = str_url.replace('\"}','')
    return str_url

def _Get_Tracks_In_Album(str):
    dict_album = spotify.album_tracks(str)
    df_album = pd.DataFrame(dict_album)
    df_album = df_album['items']
    df_album = pd.DataFrame(df_album)
    df_tracks = df_album.applymap(Get_TrackId_From_Tracks)
    return df_tracks

def AlbumId_To_TrackId(add_df) :
    df = pd.DataFrame()
    df_tracks = add_df.applymap(_Get_Tracks_In_Album)
    leng = len(df_tracks)
    for i in range(leng) :
        df_an_album = df_tracks.iat[i,0]
        df = pd.concat([df,df_an_album],ignore_index=True)
    return df

def split_list(list):
    for i in range(0, len(list), 100):
        yield list[i:i+100]

def make_playlist(df):
    play_list_dict = spotify.user_playlist_create(user = username, name=date)
    play_list_url = play_list_dict['external_urls']
    play_list_url = json.dumps(play_list_url)
    str_url = play_list_url.replace('{\"spotify\": "','')
    str_url = str_url.replace('\"}','')
    list = df["items"].to_list()
    list_split_trackid = split_list(list)
    for list in list_split_trackid:
        spotify.user_playlist_add_tracks(username, str_url, list)

if __name__ == "__main__":
    main()
