from Song import Song
import Config
from youtube_search import YoutubeSearch
import clipboard
import csv

def dict_to_song(data:dict) -> Song:
    is_valid = True
    for prop in data:
        if not prop in data:
            is_valid = False
            break
    if not is_valid:
        return None
    return Song(data['id'], data['title'], data['channel'], data['duration']) # create and return a song object

def link_from_playlist(playlist:list) -> str:
    if not playlist:
        return Config.ErrorStr
    return Config.PlaylistPrefix + ",".join([song.get_prop("id") for song in playlist])

def youtify(csv_filename:str) -> list:

    search_terms = []

    with open(csv_filename, 'r') as data:
        for line in csv.DictReader(data):
            song = line['Track Name'] + " " + line['Artist Name(s)']
            search_terms.append(song)

    # search and store all songs, comma seperated
    songs = []

    for term in search_terms:
        results = YoutubeSearch(term, max_results=1).to_dict()
        new_song = Song(results[0]["id"], results[0]["title"], results[0]["channel"], results[0]["duration"])
        songs.append(new_song)

    return songs