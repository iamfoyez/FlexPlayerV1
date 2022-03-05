import Config

class Song:

    def is_prop(prop:str) -> bool:
        return prop in Config.SongProperties

    # NON - STATIC 

    def __init__(self, id:str, title:str, channel:str, duration:str) -> None:
        self.__data = {
            "id" :  id,
            "title" : title,
            "channel" : channel,
            "duration" : duration
        }
    
    def __str__(self) -> str:
        return self.get_one_liner()
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, Song) and self.__data["id"] is o.__data["id"]
    
    def __len__(self) -> int:
        time_arr = [ int(t) for t in self.__data['duration'].split(":") ]
        time_arr.reverse()
        seconds = 0
        for i in range(len(time_arr)):
            seconds += (60 ** i) * time_arr[i]
        return seconds
    
    # GETTER METHODS

    def get_prop(self, prop:str) -> str:
        # change `prop` to lower
        prop = prop.lower()
        return self.__data[prop] if Song.is_prop(prop) else Config.ErrorStr
    
    def get_export(self) -> dict:
        return self.__data
    
    def get_link(self) -> str:
        return "https://www.youtube.com/watch?v=" + self.__data["id"]
    
    def get_one_liner(self) -> str:
        return "{} - {} - {}".format(self.__data["channel"], self.__data["title"], self.__data["duration"])