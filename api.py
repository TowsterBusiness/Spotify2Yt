import json
import requests
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

YT_KEY = "<INSERT>"
SPOTIFY_CLIENT_ID = "<INSERT>"
SPOTIFY_KEY = "<INSERT>"

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def yt_search(keywords: str):
    youtube = build("youtube", "v3", developerKey=YT_KEY)
    req = youtube.search().list(
        part="snippet",
        q=keywords,
        type="video",
        maxResults=1,

    )
    response = req.execute()

    return response


def get_yt_cred():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    yt = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return yt


def make_playlist(name: str, yt):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if (yt == None):
        yt = get_yt_cred()

    request = yt.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": name
            }
        }
    )
    response = request.execute()

    return response


def add_song(playlistId: str, songId: str, yt):
    if (yt == None):
        yt = get_yt_cred()

    request = yt.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlistId,
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": songId
                }
            }
        }
    )
    response = request.execute()

    return response


def get_spotify_playlist(link: str):

    if (not link.startswith('https://')):
        print("Invalid Link")

    if (link.find("?") != -1):
        link = link.removesuffix(link[link.find("?"): len(link)])
        print("trunkated link to: ", link)
    while link.find("/") != -1:
        link = link.removeprefix(link[0: link.find("/") + 1])
        print("trunkated link to: ", link)

    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_KEY)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("got spotify manager")

    full_list = []
    playlist = sp.playlist_items(link)
    offset = 0
    
    print("running through: ", playlist, " with offset:", offset)
    for i in range(len(playlist["items"])):
        full_list.append(playlist["items"][i])
    offset += 100
    playlist = sp.playlist_items(link, offset=offset)
    
    while playlist['offset'] == playlist['total']:
        
        print("running through: ", playlist, " with offset:", offset)
        for i in range(len(playlist["items"])):
            full_list.append(playlist["items"][i])
        offset += 100
        playlist = sp.playlist_items(link, offset=offset)
        
    return full_list
