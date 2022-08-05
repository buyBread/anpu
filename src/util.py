import json
import os
import sys

from pathlib import Path as path

def print_indented(x):
    print(json.dumps(x, sort_keys=True, indent=4))

def get_home_folder():
    return str(path.home())
    
def get_config_folder():
    if sys.platform == "linux":
        config_folder = get_home_folder() + "/.config/anpu"
    elif "win" in sys.platform:
        # i didn't know this existed, wow
        config_folder = gos.getenv("APPDATA") + "/anpu"
    elif sys.platform == "darwin":
        # i have no clue how macos works
        config_folder = get_home_folder() + "/Library/Preferences/anpu"
    else:
        exit("Couldn't find the config folder.")

    if not os.path.exists(config_folder):
        try:
            os.makedirs(config_folder)
        except Exception as e: # probably impossible given where we're trying to write
            exit(f"Can't create config folder.\n{e}")

    return config_folder

def get_config():
    config_file = str(get_config_folder() + "/config.json")

    if not os.path.exists(config_file):
        with open(config_file, "w") as fp: # surely if we can make a folder, we're allowed to create a file there
            json.dump({ "client_id": "", "client_secret": "", "current_token": "" }, fp, indent=4)

    return config_file

def filter_track_json(track):
    filtered = {}

    filtered["album"] = {}
    filtered["album"]["name"] = track["album"]["name"]
    filtered["album"]["image"] = track["album"]["images"][0]["url"] # first is the biggest (usually 640x640)
    filtered["album"]["release_date"] = track["album"]["release_date"]

    filtered["artist"] = track["artists"][0]["name"] # first is the actual artist (even if in an album by another artist)
    filtered["name"] = track["name"]
    filtered["explicit"] = track["explicit"]
    filtered["duration_ms"] = track["duration_ms"]
    filtered["track_number"] = track["track_number"] # in album

    return filtered

def filter_album_json(album):
    filtered = {}

    filtered["name"] = album["name"]
    filtered["image"] = album["images"][0]["url"]
    filtered["release_date"] = album["release_date"]

    filtered["tracks"] = []

    for track in album["tracks"]["items"]:
        idx = len(filtered["tracks"])
        filtered["tracks"].append({})

        filtered["tracks"][idx]["artist"] = track["artists"][0]["name"]
        filtered["tracks"][idx]["name"] = track["name"]
        filtered["tracks"][idx]["explicit"] = track["explicit"]
        filtered["tracks"][idx]["duration_ms"] = track["duration_ms"]
        filtered["tracks"][idx]["track_number"] = track["track_number"]

    return filtered
