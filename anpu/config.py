import json
import os
import sys

from pathlib import Path as path
    
def get_home_folder():
    return str(path.home())
    
def get_config_folder():
    if sys.platform == "linux":
        config_folder = get_home_folder() + "/.config/anpu"
    elif "win" in sys.platform:
        # i didn't know this existed, wow
        config_folder = os.getenv("APPDATA") + "/anpu"
    elif sys.platform == "darwin":
        # i have no clue how macos works
        config_folder = get_home_folder() + "/Library/Preferences/anpu"
    else:
        exit("Anpu isn't supported.")

    if not os.path.exists(config_folder):
        try:
            os.makedirs(config_folder)
        except Exception as e: # probably impossible given where we're trying to write
            exit(f"Anpu can't create config folder.\n{e}")

    return config_folder

def get_config():
    config_file = str(get_config_folder() + "/config.json")

    if not os.path.exists(config_file):
        with open(config_file, "w") as fp: # surely if we can make a folder, we're allowed to create a file there
            json.dump({ "client_id": "", "client_secret": "", "current_token": "" }, fp, indent=4)

    return config_file
