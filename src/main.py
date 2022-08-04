import sys
import json
import spotify
import util

if __name__ == "__main__":
    with open(util.get_config(), "r") as fp:
        data = json.load(fp)

        if data["client_id"] == "" or data["client_secret"] == "":
            data["client_id"] = input("Enter your Spotify App's client ID: ")
            data["client_secret"] = input("Enter your Spotify App's client secret: ")
            data["current_token"] = "" # just in case

            with open(util.get_config(), "w") as w_fp:
                json.dump(data, w_fp, indent=4)

    # argparser looks annoying
    args = sys.argv
    args.pop(0)

    if len(args) == 0:
        exit(
"""
    Anpu (暗譜)

usage: anpu <options> <query>
       anpu <link>

Options:
    --track, -t                    Set search query type for tracks (default).
    --album, -a                    Set search query type for albums.
"""
        )

    client = spotify.client(
        data["client_id"],
        data["client_secret"])

    # is a link being parsed?
    if any(x in args[0] for x in ("http", "www")):
        req = args[0]
    else:
        query_type = "track"
        query_limit = 10 # realistically speaking even this is too much,
                         # but just in case the song still doesn't appear..

        options = {
            "--track": "track",
            "-t": "track",
            "--album": "album",
            "-a": "album",
        }

        query = []

        for arg in args:
            if arg not in options:
                query.append(arg)
                continue

            query_type = options[arg]

        query = " ".join(x for x in query)

        req = {
            "q": query,
            "type": query_type,
            "limit": query_limit,
        }

    # TODO:
    # - Display a cohesive print out of our result.
    # - Search the result(s) via youtube-dl with the titles and artists
    #   (match the duration too so we don't accidentally grab a wrong result)
    # - Download the matched result(s) to the "Music" folder.

    print(client.send_request(req))
