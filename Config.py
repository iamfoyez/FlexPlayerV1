from Song import Song


db_dir = "db.json"
SongProperties = ["id", "title", "channel", "duration"]
ErrorStr = "n/a"
IntInputRange = (0,0)
EOF = ".."
BrowseSearchLength = 15
Message = {
    "goodbye": "Hope you have a great day!",
    "no-search-result": "No such song found! Going back to main menu!"
}
RandomNameLength = 10
InputCursor = "> "
db = {
    "all-songs": "all-songs.json",
    "all-playlist": "all-playlists.json"
}
default_volume = 50
SearchProperty = "title"
Menu = {
    "Play": {
        "All Songs": {
            "Play": "Play All Songs",
            "Shuffle": "Shuffle all the songs",
            "Search": "Search through all the songs"
        },
        "Playlist": {
            "Play": "Play All Songs",
            "Shuffle": "Shuffle all the songs",
            "Search": "Search through all the songs"
        }
    },
    "Add Song": {
        "To Playlist": "Add songs to a playlist",
        "To All Songs": "Add songs to all songs collection",
        "To Both": "Add both to the songs and a playlist"
    },
    "Manage Playlist": {
        "View Playlist": "Browser a Playlist",
        "Delete Playlist": "Delete a playlist"
    },
    "Browse YouTube": "Search and play music by yourself!",
    "Youtify": "Add songs from a Spotify Playlist"
}
PlaylistPrefix = "http://www.youtube.com/watch_videos?video_ids="
default_song = Song("8dAqV6pNaaU", "Future & Lil Uzi Vert - Over Your Head [Official Music Video]", "LIL UZI VERT", "3:19")