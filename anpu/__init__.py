import requests
import inspect
import json
import sys
import os

from urllib.parse import urlencode
from base64 import b64encode
from time import sleep
from pathlib import Path as path
    
def get_config_folder():
    if sys.platform == "linux":
        config_folder = str(path.home()) + "/.config/anpu"
    elif "win" in sys.platform:
        config_folder = os.getenv("APPDATA") + "/anpu"
    elif sys.platform == "darwin":
        config_folder = str(path.home()) + "/Library/Preferences/anpu"
    else:
        exit("Anpu isn't supported.")

    if not os.path.exists(config_folder):
        try:
            os.makedirs(config_folder)
        except Exception as e:
            exit(f"Anpu can't create the config folder.\n{e}")

    return config_folder

def get_config():
    config_file = get_config_folder() + "/config.json"

    if not os.path.exists(config_file):
        with open(config_file, "w") as fp:
            json.dump({ "client_id": "", "client_secret": "", "current_token": "" }, fp, indent=4)

    return config_file

class client():
    """
    The Anpu "client" is a small class with only one public method `send_request`.

    All other methods and class variables are private and are not meant to be used outside the class.

    Parameters
    ----------
    id: Optional [:class:`str`]
        Your Spotify App's ID. If none is provided the ID is taken from the config file.
    secret: Optional [:class:`str`]
        Your Spotify App's Secret. If none is provided the ID is taken from the config file.
    debug: Optional [:class:`bool`]
        Whether the client is run in Debug mode or not. Default is False. If True the `__log_activity` function will print relevant information.
    """
    def __init__(self, id=None, secret=None, debug=False):
        with open(get_config(), "r") as fp:
            self._config = json.load(fp)

        # app credentials
        if id == None:
            self._id = self._config["client_id"]
            if self._id == "":
                exit("Client ID is missing. Either provide it directly or edit the config file.")
        else:
            self._id = id

        if secret == None:
            self._secret = self._config["client_secret"]
            if self._secret == "":
                exit("Client Secret is missing. Either provide it directly or edit the config file.")
        else:
            self._secret = secret

        self._access_token = self._config["current_token"]

        self._debug = debug # False = no printing

        # control
        self._request_access_token = False
        self._can_continue = True

        self._request = None

        self._responses = {
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "OK, but there's no content",
            304: "Modified",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            429: "Too many Requests",
            500: "Internal Server error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }

    def __log_activity(self, msg):
        if self._debug:
            last_frame = inspect.currentframe().f_back
            print(f"{inspect.getframeinfo(last_frame)[2]}(): {msg}")

    def __handle_status_code(self):
        response = self._responses.get(self._request.status_code, "Unknown")

        if self._request.status_code == 200:
            self._can_continue = True
        else:
            self._can_continue = False

        if self._request.status_code == 401:
            self._request_access_token = True
        else:
            self._request_access_token = False

        return f"Response: {self._request.status_code} {response}."

    def __acquire_access_token(self):
        if self._request_access_token or self._access_token == "":
            credentials = b64encode(
                f"{self._id}:{self._secret}".encode())

            r = requests.post(
                url="https://accounts.spotify.com/api/token",
                data={ "grant_type": "client_credentials" },
                headers={ "Authorization": f"Basic {credentials.decode()}" })

            self.__log_activity(
                f"Response: {r.status_code} {self._responses.get(r.status_code, 'Unknown')}")

            if r.status_code != 200:
                exit("Anpu cannot acquire a new Access Token.")

            self._config["current_token"] = r.json()["access_token"]
            self._access_token = r.json()["access_token"]
            
            # write new token
            with open(get_config(), "w") as fp:
                json.dump(self._config, fp, indent=4)
            
            return self._config["current_token"]
        
        return self._access_token

    def __make_get_request(self, url):
        if url == None:
            return False

        self._request = requests.get(
            url=url, headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})
        self.__log_activity(self.__handle_status_code())

        retries = 0

        while True:
            if retries > 5:
                self.__log_activity("Failed after 5 retries.")
                return False

            if self._can_continue:
                return True

            sleep(1)

            self.__log_activity("Retrying...")

            self._request = requests.get(
                url=url, headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})
            self.__log_activity(self.__handle_status_code())

            retries += 1

    def __figure_out_url(self, req):
        base_url = "https://api.spotify.com/v1"

        if "api.spotify.com" in req:
            self.__log_activity("Not sure why you're doing this, but I'm not stopping you.")
            return req

        if type(req) == str:
            if "spotify.com" not in req:
                self.__log_activity("Your string is not a link.")
                return None

            # no clue why you have that at the end when copying from spotify
            id = req.split("/")[len(req.split("/")) - 1]
            if "?" in id:
                id = id.split("?")[0] 

            if "track" in req:
                url = f"{base_url}/tracks/{id}"
            elif "playlist" in req:
                url = f"{base_url}/playlists{id}"
            elif "album" in req:
                url = f"{base_url}/albums{id}"
            else:
                self.__log_activity("Invalid link. Only track, album and playlist links are supported.")
                return None

            if base_url in req: # for when the reqest is already a valid API call
                url = req
        elif type(req) == dict:
            if "q" not in req:
                self.__log_activity("Your dict has no query.")
                return None
                
            url = f"{base_url}/search?{urlencode(req)}"

        return url

    def send_request(self, req):
        """
        Tells the client to send a GET request to Spotify.

        Parameters
        ----------
        req: [:class:`str`] or [:class:`dict`]
            Based on what class this is a different GET request will be sent. If sending a string, make sure it is a valid Spotify link to a track, album or playlist. Otherwise construct a [:class:`dict`] while referencing [this](https://developer.spotify.com/documentation/web-api/reference/#/operations/search).
        """
        if self.__make_get_request(self.__figure_out_url(req)):
            return self._request.json()
        else:
            return None
