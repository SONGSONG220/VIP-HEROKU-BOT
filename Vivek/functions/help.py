# This Bothelp function taken from < https://github.com/The-HellBot/Plugins >
# Credit goes to The-HellBot.
#
from ..core import app

BOT_CMD_INFO = {}
BOT_CMD_MENU = {}
BOT_HELP = {}

SYMBOLS = {
    "arrow_left": "«",
    "arrow_right": "»",
    "back": "🔙 back",
    "check_mark": "✔",
    "close": "🗑️",
    "cross_mark": "✘",
    "next": "⤚ next",
    "previous": "prev ⤙",
    "radio_select": "◉",
    "radio_unselect": "〇",
}


class BotHelp:
    def __init__(self, file: str) -> None:
        self.category = file
        self.command_dict = {}
        self.command_info = ""

    def add(self, command: str, description: str):
        self.command_dict[command] = {"command": command, "description": description}
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**Plugin Category:** `{self.category}`"
        if self.command_info:
            result += f"\n**Plugin info:** __{self.command_info}__"
        result += "\n\n"
        for command in self.command_dict:
            command = self.command_dict[command]
            result += (
                f"**{SYMBOLS['radio_select']} Command:** `/{command['command']}`\n"
            )
            if command["description"]:
                result += f"**{SYMBOLS['arrow_right']} Description:** __{command['description']}__\n"
            result += "\n"

            BOT_CMD_INFO[command["command"]] = {
                "command": command["command"],
                "description": command["description"],
                "category": self.category,
            }

        return result

    def done(self) -> None:
        BOT_HELP[self.category] = {
            "commands": self.command_dict,
            "info": self.command_info,
        }
        BOT_CMD_MENU[self.category] = self.get_menu()


app.help = BotHelp
