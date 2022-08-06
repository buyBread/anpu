#### Anpu (暗譜) - memorize or play a song from memory. 

A small library to search Spotify music.  
```
python -m pip install anpu
```

### Features
* Cleans up Spotify Links into API calls (tracks, albums and playlists only)
* [Query search](https://developer.spotify.com/documentation/web-api/reference/#/operations/search)

### Requirements
* `requests`
```
python -m pip install -U requests
```

### Config
Anpu requires the use of a config file to store the Access Token. The config file can also be used to store your App's credentials.  
It is automatically created in these directories respectively:
* **GNU/Linux**: `HOME/.config/anpu/config.json`
* **macOS**: `HOME/Library/Preferences/anpu/config.json`
* **Windows**: `%APPDATA%/anpu/config.json`

### Example
```py
import anpu

client = anpu.client()
# alternatively
client = anpu.client(
    id = "app_id",
    secret = "app_secret"
)

# search query
print(client.send_request(
    {
        "q": "very intresting query",
        "type": "track",
        "limit": 5
    }
))

# get by link
print(client.send_request(
    "https://open.spotify.com/track/veryrealtrackid"
))
```
