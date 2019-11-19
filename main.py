import os
import sys
import random
import logging

from collections import defaultdict, deque
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get('TOKEN')

from utils import next_talks


def get_next_talks_handler(bot, update):
    username = update.message.from_user.first_name
    proximas_charlas = next_talks()
    update.message.reply_text(f'Las próximas charlas son: {proximas_charlas}')


def level_response_handler(bot, update):
    query = update.callback_query
    proximas_charlas = next_talks()
    query.edit_message_text(text=f"La/s próxima/s charla/s nivel {proximas_charlas}:")


def ask_talk_level_handler(bot, update):
    keyboard = [[InlineKeyboardButton("Inicial", callback_data='1'),
                 InlineKeyboardButton("Intermedio", callback_data='2'),
                 InlineKeyboardButton("Avanzado", callback_data='3'),
                 InlineKeyboardButton("Todas", callback_data='4') ] ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('De qué nivel te gustaría?', reply_markup=reply_markup)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('y_ahora', get_next_talks_handler))
updater.dispatcher.add_handler(CommandHandler('actividades', ask_talk_level_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(level_response_handler))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
