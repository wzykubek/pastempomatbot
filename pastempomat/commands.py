from telegram import Update
from telegram.ext import CallbackContext
from tinydb import Query as DBQuery
from . import bot, db
from .config import ADMINS


@bot.command("paste_add")
def paste_add(update: Update, context: CallbackContext):
    if update.message.from_user.username not in ADMINS:
        update.message.reply_text("Nie masz uprawnień do dodawania nowych past.")
        return
    if not context.args:
        update.message.reply_text("Podaj nazwę dla tej pasty.")
        return

    name = " ".join(context.args)
    content = (
        update.message["reply_to_message"]["text"]
        .replace("_", "\\_")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )

    p = DBQuery()
    if len(db.search(p.name == name)) == 0:
        db.insert({"name": name, "content": content})
        update.message.reply_text(f'Dodano pastę o nazwie "{name}".')
    else:
        update.message.reply_text("Pasta o takiej nazwie już istnieje.")
        


@bot.custom_help_command
def start(update: Update, context: CallbackContext, desc: dict):
    update.message.reply_text(
        """
Bot, który postuje pasty.

Aby użyć bota zacznij wpisywać:
@pastempomatbot <szukana_pasta>
a następnie kliknij wybraną by ją wysłać.
"""
    )
