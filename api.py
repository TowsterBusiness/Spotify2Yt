
from googleapiclient.discovery import build
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