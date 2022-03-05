from tinydb import TinyDB, Query, table, where
import Config
from Song import Song
from Util import dict_to_song

class Database:

    def __init__(self) -> None:
        self.__db = TinyDB(Config.db_dir)
        self.__playlists = {}
        self.__load_db()

    # PRIVATE METHODS

    def __load_db(self):
        # make one db for all songs
        if not "all-songs" in self.__db.tables():
            self.add_to_playlist("all-songs", Config.default_song)
        else:
            for playlist_name in self.__db.tables():
                self.__playlists[playlist_name] = self.__db.table(playlist_name)

    # GETTERS
    
    def get_playlist_names(self) -> list:
        playlists = []
        for playlist_name in self.__db.tables():
            playlists.append(playlist_name)
        return playlists
    
    def get_playlist(self, playlist_name:str) -> list:
        playlist = self.__db.table(playlist_name).all()
        if not playlist:
            return []
        search_result = []
        for song in playlist:
            search_result.append(dict_to_song(song))
        return search_result
        

    # SETTERS

    def make_playlist(self, name:str) -> bool:
        name = name.strip()
        if not name:
            return False
        if name in self.__db.tables():
            return False
        self.__playlists[name] = self.__db.table(name)
        return True
    
    def add_to_playlist(self, playlist_name:str, song:Song) -> bool:
        if not playlist_name in self.__db.tables():
            self.make_playlist(playlist_name)
        search = self.search(playlist_name, song.get_prop("id"), "id")
        if not search:
            self.__playlists[playlist_name].insert(song.get_export())

            if not playlist_name == "all-songs":
                search = self.search("all-songs", song.get_prop("id"), "id")
                if not search:
                    self.__playlists["all-songs"].insert(song.get_export())
                    
            return True
        return False
    
    def search(self, playlist_name:str, term:str, prop:str = Config.SearchProperty) -> list:
        if not prop in Config.SongProperties:
            return []
        if playlist_name in self.__db.tables():
            search_func = lambda title: term.lower() in title.lower()
            results = self.__playlists[playlist_name].search(where(prop).test(search_func))
            if not results:
                return []
            search_result = []
            for song in results:
                search_result.append(dict_to_song(song))
            return search_result
        else:
            return []
    
    def delete_playlist(self, playlist_name:str) -> bool:
        if playlist_name in self.__db.tables():
            self.__db.drop_table(playlist_name)
            return True
        return False