import os
import sys
from collections import defaultdict, deque

from telegram.ext import Updater, CommandHandler, MessageHandler

from constants import TRIGGERS


TOKEN = '742576280:AAH5iPOg5WHIgDrt'

def process_message(bot, update):
    chat_id = update.message.chat.id
    message_content = update.message.text
    if message_content[0] != ['/']:      
        message_content_lower = message_content.lower()
        triggered_content = list(filter(message_content_lower.__contains__, TRIGGERS.keys()))
        reply_message_content = TRIGGERS[triggered_content[0]]
        username = update.message.from_user.first_name
        update.message.reply_text(f'{reply_message_content} {username}')


def aceptar_cachivache(bot, update):
    username = update.message.from_user.first_name
    update.message.reply_text(f'🙋‍♂️A mi me sirve {username} Gracias!')

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('quienquiere', aceptar_cachivache))
updater.dispatcher.add_handler(MessageHandler(None,callback=process_message))

updater.start_polling()
updater.idle()