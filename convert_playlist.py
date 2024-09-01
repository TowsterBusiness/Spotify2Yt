from api import *
import json
import sys

playlist_name = "Alyssa's Emo Playlist"
spotify_playlist_link = "https://open.spotify.com/playlist/4U3luFV3uWZWIjJUcjsiFK?si=3fc4353925fb43fa"
save_object = None


def main():
    global playlist_name
    global spotify_playlist_link
    global save_object
    
    # get playlist This is Isabella's playlist
    playlist = get_spotify_playlist(
        spotify_playlist_link)
    print("Got playlist from Spotify")

    # Get YT Credits
    yt = get_yt_cred()
    print("Got yt cred")

    with open('save.json', 'r') as openfile:
        save_object = json.load(openfile)
    print("Got save data with: ", save_object)

    if (save_object["state"] < 0):
        for spo_song in playlist:
            search_term = spo_song["track"]["name"]

            for song_writer in spo_song["track"]["artists"]:
                search_term = search_term + " " + song_writer["name"]

            save_object["search_terms"].append(search_term)
        save_object["state"] = 0
        save_file()

    if (save_object["state"] < 1):
        while len(save_object["search_terms"]) != 0:
            search_term = save_object["search_terms"].pop()
            try:
                search_response = yt_search(str(search_term))
                print(search_term)
                if (len(search_response["items"]) == 0):
                    print("couldn't add: %s to the playlist" % search_term)
                else:
                    save_object["yt_ids"].append(
                        search_response["items"][0]["id"]["videoId"])
            except Exception as err:
                save_object["search_terms"].append(search_term)
                save_file()
                sys.exit()
        save_object["state"] = 1
        save_file()

    if (save_object["state"] < 2):
        try:
            playlist_response = make_playlist(playlist_name, yt)
            print(json.dumps(playlist_response, indent=3))
            save_object["playlist_id"] = playlist_response["id"]
            save_object["state"] = 2
            save_file()
        except Exception as err:
            print(type(err))
            print(err.args)
            print(err)
            sys.exit()

    error_count = 0
    while len(save_object["yt_ids"]) != 0:
        song_id = save_object["yt_ids"].pop()
        try:
            print(song_id)
            add_song(save_object["playlist_id"], song_id, yt)
        except Exception as err:
            save_object["yt_ids"].append(song_id)
            save_object["state"] = 2
            save_file()
            error_count += 1
            if (error_count > 10):
                sys.exit()
    save_object["state"] = -1
    save_file()


def save_file():
    global save_object
    with open("save.json", "w") as out_file:
        out_file.write(json.dumps(save_object, indent=4))


if __name__ == "__main__":
    main()
