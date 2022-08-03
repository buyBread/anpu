import requests
import json

from urllib.parse import urlencode
from base64 import b64encode

class client:
    def __init__(self):
        self.access_token_expired = False

    def print_status_code(self, status_code, func):
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

        print(f"{func}(): Request: {responses.get(status_code, 'Unknown')}.")

    def __acquire_access_token(self):
        data = None

        with open("../config.json", "r") as fp:
            data = json.load(fp)

            if data["current_token"] == "":
                print("__acquire_access_token(): Access Token not present.")
                self.access_token_expired = True

        if self.access_token_expired:
            print("__acquire_access_token(): Requesting a new Access Token.")

            with open("../config.json", "r") as fp:
                data = json.load(fp)
                credentials = b64encode(
                    f"{data['client_id']}:{data['client_secret']}".encode())

                r = requests.post(
                    url="https://accounts.spotify.com/api/token",
                    data={ "grant_type": "client_credentials" },
                    headers={ "Authorization": f"Basic {credentials.decode()}" })

            self.print_status_code(r.status_code, "__acquire_access_token")

            if (r.status_code != 200):
                return "Failed."
            
            print("__acquire_access_token(): Access Token acquired!")

            with open("../config.json", "r") as fp:
                data = json.load(fp)
                data["current_token"] = r.json()["access_token"]
            
            # because "r+" appends?
            with open("../config.json", "w") as fp:
                json.dump(data, fp, indent=4)

            self.access_token_expired = False
            
            return data["current_token"]
        else:
            return data["current_token"]

    def search_link(self, link):
        if "track" in link:
            url = "https://api.spotify.com/v1/tracks"
        elif "playlist" in link:
            url = "https://api.spotify.com/v1/playlists"
        elif "album" in link:
            url = "https://api.spotify.com/v1/albums"
        else:
            print("search_link(): Invalid link.")

        link = link.split("/")
        id = link[len(link) - 1]
        if "?" in id:
            id = id.split("?")[0]

        r = requests.get(
            url=f"{url}/{id}",
            headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

        self.print_status_code(r.status_code, "search_link")

        if r.status_code == 401: # expired or invalid token
            print("search_link(): Access Token has expired or is invalid.")

            self.access_token_expired = True

            r = requests.get(
                url=f"{url}/{id}",
                headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

        if r.status_code == 400:
            print("search_link(): Invalid ID.")
            return

        if r.status_code == 404:
            return

        print("search_link(): Complete!")

        return r.json()

    def search_query(self, req):
        r = requests.get(
            url=f"https://api.spotify.com/v1/search?{urlencode(req)}",
            headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

        self.print_status_code(r.status_code, "search_query")

        if r.status_code == 401: # expired or invalid token
            print("search_query(): Access Token has expired or is invalid.")

            self.access_token_expired = True

            r = requests.get(
                url=f"https://api.spotify.com/v1/search?{urlencode(req)}",
                headers={"Authorization": f"Bearer {self.__acquire_access_token()}"})

        print("search_query(): Complete!")

        return r.json()
