import json
import os
import sys

from pathlib import Path as path

def print_indented(x):
    print(json.dumps(x, sort_keys=True, indent=4))
    
def get_config_folder():
    if sys.platform == "linux":
        config_folder = str(path.home()) + "/.config/anpu"
    elif "win" in sys.platform:
        config_folder = str(path.home()) + "/anpu"
    elif sys.platform == "darwin":
        # i have no clue how macos works
        config_folder = str(path.home()) + "/Library/Preferences/anpu"
    else:
        exit("Couldn't find the config folder.")

    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    return config_folder

def get_config():
    config_file = str(get_config_folder() + "/config.json")

    if not os.path.exists(config_file):
        with open(config_file, "w") as fp:
            json.dump({ "client_id": "", "client_secret": "", "current_token": "" }, fp, indent=4)

    return config_file
