import Config

class UserInput:

    def __init__(self) -> None:
        pass

    def get_int(self, prompt = "", cursor = Config.InputCursor, range = (0,0)):
        print(prompt) if prompt else ""
        user_input = input(cursor)
        if user_input == Config.EOF:
            return Config.EOF
        if user_input.isnumeric():
            user_input = int(user_input)
            return user_input if range == Config.IntInputRange else user_input if user_input >= range[0] and user_input <= range[1] else self.get_int(prompt, cursor, range)
        else:
            return self.get_int(prompt, cursor, range)
    
    def get_str(self, prompt = "", cursor = "> ", new_line = True, allow_empty=False):
        if prompt:
            if new_line:
                print(prompt)
            else:
                print(prompt, end="")
        user_input = input(cursor)
        if user_input == Config.EOF:
            return Config.EOF
        return str(user_input.strip()) if allow_empty else str(user_input.strip()) if user_input.strip() else self.get_str(prompt, cursor=cursor, new_line=new_line, allow_empty=allow_empty)
    
    def get_menu_selection(self, screen:str, current = "", selection_arr:list=[]) -> list:
        if screen == "root":
            current = Config.Menu
        string = ""
        options = []
        for i, option in enumerate(current):
            string += "{}) {}\n".format(i + 1, option)
            options.append(option)
        string = string.strip()
        selection = self.get_int(string, range = (1, len(current)))

        if selection == Config.EOF:
            if screen == "root":
                return []
            else:
                selection_arr.pop()
                screen = selection_arr[-1] if len(selection_arr) >= 1 else "root"
                current = Config.Menu
                for x in selection_arr:
                    current = current[x]
                return self.get_menu_selection(screen, current = current)
        else:
            selection_arr.append(options[selection - 1])
            current = current[options[selection - 1]]
        if type(current) == str:
            return selection_arr
        return self.get_menu_selection(options[selection - 1], current = current)
    
    def get_selection_from_list(self, options:list) -> str:
        for i, option in enumerate(options):
            print("{}) {}".format(i + 1, str(option)))
        select = self.get_int(range=(1, len(options)))
        if select == Config.EOF:
            return Config.EOF
        return options[select - 1]