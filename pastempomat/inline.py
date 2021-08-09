from telegrask import InlineQuery
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from re import IGNORECASE
from tinydb import Query as DBQuery
from . import bot, db


@bot.inline_query
def inline(query: InlineQuery):
    regex = query.query_str
    p = DBQuery()
    results = db.search(
        p.name.search(regex, flags=IGNORECASE)
        | p.content.search(regex, flags=IGNORECASE)
    )
    for result in results:
        if len(query.answers) <= 49:
            query.add_answer(
                InlineQueryResultArticle(
                    id=query.get_random_id(),
                    title=result["name"],
                    description=query.parse_description(result["content"]),
                    input_message_content=InputTextMessageContent(
                        result["content"], parse_mode=ParseMode.MARKDOWN
                    ),
                )
            )
    query.send_answers()
