import requests
import inspect
import json
import util

from urllib.parse import urlencode
from base64 import b64encode

class client:
    """
    A small Spotify "client" to handle POST requests for Access Tokens and GET requests for songs, albums and playlists.

    Has some small logging utility.
    """

    def __init__(self, id, secret, debug=True):
        # app credentials
        self.id = id
        self.secret = secret
        self.debug = debug

        self._request_access_token = False
        self._redo_request = False
        self.__status_code = None

    # TODO:
    # - Make this also handle turning off the booleans (for more automation)
    #   (honestly.. this is just for prettier code)
    def handle_status_code(self):
        responses = {
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

        if self.__status_code == 401: # expired access token
            self._request_access_token = True
            self._redo_request = True

        return f"Request Status Code: {responses.get(self.__status_code, 'Unknown')}."

    def log_activity(self, msg):
        if self.debug:
            last_frame = inspect.currentframe().f_back
            print(f"{inspect.getframeinfo(last_frame)[2]}(): {msg}")

    def __acquire_access_token(self):
        with open(util.get_config(), "r") as fp:
            data = json.load(fp)

            if data["current_token"] == "":
                self._request_access_token = True

        if self._request_access_token:
            self._request_access_token = False

            credentials = b64encode(
                f"{self.id}:{self.secret}".encode())

            r = requests.post(
                url="https://accounts.spotify.com/api/token",
                data={ "grant_type": "client_credentials" },
                headers={ "Authorization": f"Basic {credentials.decode()}" })

            self.__status_code = r.status_code

            self.log_activity(self.handle_status_code())

            if self.__status_code != 200:
                exit("Failed to request a new access token.")

            data["current_token"] = r.json()["access_token"]
            
            # because "r+" appends?
            with open(util.get_config(), "w") as fp:
                json.dump(data, fp, indent=4)
            
            return data["current_token"]
        
        return data["current_token"]

    def send_request(self, req):
        base_url = "https://api.spotify.com/v1"

        if type(req) == str:
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
                self.log_activity("Invalid link. Only track, album and playlist links are supported.")
                return

            if base_url in req: # for when the reqest is already a valid API call
                url = req
        elif type(req) == dict:
            url = f"{base_url}/search?{urlencode(req)}"
        else:
            self.log_activity("How did this even happen?\n`req`:\n{req}")
            return

        r = requests.get(
            url=url, headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

        self.__status_code = r.status_code

        self.log_activity(self.handle_status_code())

        if self._redo_request:
            r = requests.get(
                url=url, headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

            self.__status_code = r.status_code

            self.log_activity(self.handle_status_code())

        if self.__status_code != 200: # let's say, hypothetically, everything was ok
            self.log_activity(self.handle_status_code())
            return

        return r.json()
