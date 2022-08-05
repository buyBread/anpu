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

    response = client.send_request(req)
    #util.print_indented(response)

    results = []

    if any(x in response for x in ("albums", "tracks")):
        category = query_type + "s"
        
        for item in response[category]["items"]:
            idx = len(results)
            results.append({})

            if category == "tracks":
                results[idx] = util.filter_track_json(item)

            if category == "albums":
                # we'll filter a lot more data later
                results[idx]["name"] = item["name"]
                results[idx]["image"] = item["images"][0]["url"]
                results[idx]["artist"] = item["artists"][0]["name"]
                results[idx]["href"] = item["href"] # because there's no tracks in this request

        if len(results) < 10:
            print("There isn't a lot of results for this query.")

        # we're only doing this for queries because.. well.. 
        # if a user links something, they're certain it's the song/album they need.
        for num, item in enumerate(results):
            entry = f"{num + 1}) {item['name']}\n   Artist: {item['artist']}"

            try: # albums don't have an explicit rating apparently?
                if item["explicit"]:
                    entry += f" (Explicit)"
            except:
                pass

            print(entry)
    else:
        print("todo")
