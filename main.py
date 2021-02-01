#!/usr/bin/env python3
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    Dispatcher,
    InlineQueryHandler,
)
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    ParseMode,
)
from telegram.error import BadRequest
import logging
import json
import settings

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None


ctx = {"admins": ["samedamci"]}


def paste_add(update, context):
    if not context.args:
        update.message.reply_text("Podaj nazwę dla tej pasty.")
        return
    if update.message.from_user.username in ctx["admins"]:
        with open("./data/copypastes.json", "r") as f:
            pastes = json.loads(f.read())
        name = " ".join(context.args)
        content = (
            update.message["reply_to_message"]["text"]
            .replace("_", "\\_")
            .replace("[", "\\[")
            .replace("]", "\\]")
        )

        try:
            list(pastes).index(name)
            update.message.reply_text("Pasta o takiej nazwie już istnieje.")
            return
        except ValueError:
            pastes[name] = content
        pastes = json.dumps(pastes, indent=2)
        with open("./data/copypastes.json", "w") as f:
            f.write(pastes)
        update.message.reply_text(f'Dodano pastę o nazwie "{name}".')
    else:
        update.message.reply_text(
            f"""Nie masz uprawnień do dodawania nowych past.
            Administratorzy: {", ".join(ctx["admins"])}.
                                  """
        )


def inline(update, context):
    with open("./data/copypastes.json", "r") as f:
        pastes = json.loads(f.read())

    answers = []
    query = list(str(update.inline_query.query).split(" "))

    if query == [""]:
        for paste in list(pastes):
            content = pastes.get(paste)

            answers.append(
                InlineQueryResultArticle(
                    id=list(pastes).index(paste),
                    title=paste,
                    description=content[:32] + (content[29:] and "..."),
                    input_message_content=InputTextMessageContent(
                        content,
                        parse_mode=ParseMode.MARKDOWN,
                    ),
                )
            )
        context.bot.answer_inline_query(update.inline_query.id, answers, cache_time=0)
    else:
        answers = []
        for i in query:
            for paste in list(pastes):
                if i in paste:
                    content = pastes.get(paste)
                    try:
                        answers.append(
                            InlineQueryResultArticle(
                                id=list(pastes).index(paste),
                                title=paste,
                                description=content[:32] + (content[29:] and "..."),
                                input_message_content=InputTextMessageContent(
                                    content,
                                    parse_mode=ParseMode.MARKDOWN,
                                ),
                            )
                        )
                        context.bot.answer_inline_query(
                            update.inline_query.id, answers, cache_time=0
                        )
                    except BadRequest:
                        pass


def start(update, context):
    update.message.reply_text(
        """
Bot, który postuje pasty.

Aby użyć bota zacznij wpisywać:
@pastempomatbot <szukana_pasta>
a następnie kliknij wybraną by ją wysłać.
"""
    )


def main():
    global updater
    updater = Updater(settings.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(["start", "help"], start))
    dispatcher.add_handler(CommandHandler("paste_add", paste_add))
    dispatcher.add_handler(InlineQueryHandler(inline))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
