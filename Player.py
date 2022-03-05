import sys
import os
from Database import Database
from Song import Song
from UserInput import UserInput
from Util import link_from_playlist, youtify
import Config
import random
from youtube_search import YoutubeSearch

class Player:

    def __init__(self) -> None:
        self.__db = Database()
        self.__input = UserInput()
        while True:
            user_selection = self.__input.get_menu_selection("root")
            self.run(user_selection)
            user_selection.clear()
    
    def __play_link(self, link:str) -> None:
        os.system("mpv " + link + " --no-video")
    
    def __playlist_options(self,selection:list, playlist_name:str) -> bool:
        playlist = self.__db.get_playlist(playlist_name)
        if not playlist:
            print(Config.Message["no-search-result"])
            return False
        if "Shuffle" in selection:
            # Shuffle All Songs and then play
            random.shuffle(playlist)
            self.__play_link(link_from_playlist(playlist))
        elif "Search" in selection:
            term = self.__input.get_str("Search... ")
            if term == Config.EOF:
                return False
            playlist = self.__db.search(playlist_name, term)
            if not playlist:
                print(Config.Message['no-search-result'])
                return False
        self.__play_link(link_from_playlist(playlist))
        return True
    
    def __get_user_select_playlist(self, create_playlist:bool=False) -> str:
        if create_playlist:
            return self.__input.get_selection_from_list(["Create Playlist"] + self.__db.get_playlist_names())
        return self.__input.get_selection_from_list(self.__db.get_playlist_names())
    
    def __get_song_from_yt(self) -> Song:
        term = self.__input.get_str("Search... ")
        if term == Config.EOF:
            return None
        results = YoutubeSearch(term, Config.BrowseSearchLength).to_dict()
        songs_list = []
        for i in range(Config.BrowseSearchLength):
            new_song = Song(results[i]["id"], results[i]["title"], results[i]["channel"], results[i]["duration"])
            songs_list.append(new_song)
        select = self.__input.get_selection_from_list(songs_list)
        if select == Config.EOF:
            return None
        return select

    def run(self, user_selection:str):
        if not user_selection:
            sys.exit(Config.Message['goodbye'])
        if "All Songs" in user_selection:
            self.__playlist_options(user_selection, "all-songs")
        elif "Play" in user_selection and "Playlist" in user_selection:
            selection = self.__get_user_select_playlist()
            if selection == Config.EOF:
                return True
            self.__playlist_options(user_selection, selection)
        elif "Add Song" in user_selection:
            if "To Playlist" in user_selection:
                selection = self.__get_user_select_playlist(create_playlist=True)
                if selection == "Create Playlist":
                    selection = self.__input.get_str("Name of New Playlist ")
                if selection == Config.EOF:
                    return True 
                while True:
                    song = self.__get_song_from_yt()
                    if not song:
                        break
                    self.__db.add_to_playlist(selection, song)
            elif "To All Songs" in user_selection:
                selection = "all-songs"
                while True:
                    song = self.__get_song_from_yt()
                    if not song:
                        break
                    self.__db.add_to_playlist(selection, song)
            elif "To Both" in user_selection:
                selection = self.__get_user_select_playlist(create_playlist=True)
                if selection == "Create Playlist":
                    selection = self.__input.get_str("Name of New Playlist ")
                if selection == Config.EOF:
                    return True 
                while True:
                    song = self.__get_song_from_yt()
                    if not song:
                        break
                    self.__db.add_to_playlist(selection, song)
                    self.__db.add_to_playlist("all-songs", song)
        elif "Manage Playlist" in user_selection:
            if "View Playlist" in user_selection:
                selection = self.__get_user_select_playlist()
                if selection == Config.EOF:
                    return True
                playlist = self.__db.get_playlist(selection)
                print("\nSongs in " + selection + " : \n")
                for i, song in enumerate(playlist):
                    print("{}) {}".format(i + 1, song.get_one_liner()))
                print("")
            elif "Delete Playlist" in user_selection:
                selection = self.__get_user_select_playlist()
                if selection == Config.EOF:
                    return True
                if self.__db.delete_playlist(selection):
                    print("Deleted " + selection)
                else:
                    print("Error Deleting " + selection)
        elif "Browse YouTube" in user_selection:
            while True:
                song = self.__get_song_from_yt()
                if not song:
                    break
                self.__play_link(song.get_link())
        elif "Youtify" in user_selection:
            playlist_name = self.__input.get_str("Name of the new playlist ")
            if playlist_name == Config.EOF:
                return True
            file_name = self.__input.get_str("Path to csv file ")
            if file_name == Config.EOF:
                return True
            new_playlist = youtify(file_name)
            for song in new_playlist:
                self.__db.add_to_playlist(playlist_name, song)
            

flexplayer = Player()