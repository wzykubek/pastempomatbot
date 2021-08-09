from telegrask import Telegrask
from .config import TOKEN, DB_PATH
from tinydb import TinyDB

bot = Telegrask(TOKEN)
bot.config["HELP_MESSAGE"] = False
db = TinyDB(DB_PATH)

from . import commands, inline