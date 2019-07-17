import os
import sys
import random
import logging

from collections import defaultdict, deque
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from constants import TRIGGERS
from stickers import IAN, IAN_LEFT


TOKEN = ''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def process_message(bot, update):
    message_content = update.message.text
    if message_content[0] != ['/']:      
        message_content_lower = message_content.lower()
        triggered_content = list(filter(message_content_lower.__contains__, TRIGGERS.keys()))
        reply_message_content = TRIGGERS[triggered_content[0]]
        username = update.message.from_user.first_name
        update.message.reply_text(f'{reply_message_content} {username}')


def aceptar_cachivache(bot, update):
    username = update.message.from_user.first_name
    update.message.reply_sticker(random.choice([IAN, IAN_LEFT]))
    update.message.reply_text(f'A mi me sirve {username} Gracias!')


def preguntar_por_cachivache(bot, update):
    keyboard = [[InlineKeyboardButton("Si", callback_data='1'),
                 InlineKeyboardButton("No", callback_data='2')],
                [InlineKeyboardButton("Quizas podria usarlo", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Alguien mas lo quiere?', reply_markup=reply_markup)


def respuesta(bot, update):
    query = update.callback_query
    if query.data == '1':
        query.edit_message_text(text="Uhhhh, bueno. Lo siguiente me lo llevo")
    if query.data == '2':
        query.edit_message_text(text="Genial, mañana me lo llevo")
    if query.data == '3':
        query.edit_message_text(text="Bueno, no hay problema")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('quienquiere', aceptar_cachivache))
updater.dispatcher.add_handler(CommandHandler('alguienquiere', preguntar_por_cachivache))
updater.dispatcher.add_handler(CallbackQueryHandler(respuesta))
updater.dispatcher.add_handler(MessageHandler(None, callback=process_message))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()