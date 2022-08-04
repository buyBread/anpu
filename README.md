# Anpu
Search and Download songs, albums and playlists on Spotify using [youtube-dl](https://github.com/ytdl-org/youtube-dl/).

### Config
1. Visit https://developer.spotify.com/dashboard to create an app.
2. Run `anpu` to create and configure the config file.

*Anpu can be supplied a link or search query regardless of if you've configured it or not.*  
  
The config file is located in these directories respectively:
* **GNU/Linux**: `HOME/.config/anpu/config.json`
* **macOS**: `HOME/Library/Preferences/anpu/config.json`
* **Windows**: `%APPDATA%/anpu/config.json`
*You can also give Anpu a link or search query as the main app is run right after configuration is finished.*

### Usage
```
    Anpu (暗譜)

usage: anpu <options> <query>
       anpu <link>

Options:
    --limit, -l                    Set the query limit (default=10).
    --track, -t                    Set search query type for tracks (default).
    --album, -a                    Set search query type for albums.
```
