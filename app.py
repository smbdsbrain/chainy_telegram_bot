import logging

from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Updater
from tinydb import TinyDB, Query

file = open('token', 'r')
updater = Updater(token=file.readlines()[0])
dispatcher = updater.dispatcher

db = TinyDB('db.json')
query = Query()


def increment_key(bot, update, args):
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="You should specify key")
        return

    key = args[0]
    rows = db.search(query.key == key)
    logging.info(f"{update.message.from_user.username} incrementing {key}...")

    if rows:
        row = rows[0]
        new_value = row.get('count') + 1
        db.update({'count': new_value}, query.key == key)
    else:
        new_value = 1
        db.insert({'key': key, 'count': new_value})

    bot.send_message(chat_id=update.message.chat_id, text=f"Successfully incremented, now it's {new_value}")


def get_value(bot, update, args):
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="You should specify key")
        return
    key = args[0]
    rows = db.search(query.key == key)
    logging.info(f"{update.message.from_user.username} getting {key}...")

    if rows:
        row = rows[0]
        bot.send_message(chat_id=update.message.chat_id, text=f"Now it's value is {row.get('count')}")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=f"Nobody has added this key yet and now it's 0.")


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="It's bot, which can store values and share it with anybody. \n"
                          "Don't store anything secret in values, because everybody can change it. \n"
                          "There is two commands: \n"
                          "`/increment_key key` - increment value by key \n"
                          "`/get_value key` - get value by key \n"
                          "\n"
                          "Example:\n"
                          "`/increment_key chainy` \n"
                          "`/get_value chainy` \n",
                     parse_mode=ParseMode.MARKDOWN)


start_handler = CommandHandler('start', help)
increment_key_handler = CommandHandler('increment_key', increment_key, pass_args=True)
get_value_handler = CommandHandler('get_value', get_value, pass_args=True)
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(increment_key_handler)
dispatcher.add_handler(get_value_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()
