import os
import sys
from collections import defaultdict, deque

from telegram.ext import Updater, CommandHandler, MessageHandler

from utils import obtener_dias_wfh, quitar_dia_wfh

TOKEN = os.environ.get('TOKEN')

OBTENER_DIAS_WFH = 'obtener_dias_wfh'
TOMAR_DIA_WFH = 'tomar_dia_wfh'

METHODS = {
        TOMAR_DIA_WFH: quitar_dia_wfh,
        OBTENER_DIAS_WFH: obtener_dias_wfh
        }

def micoop_test(bot, update):
    update.message.reply_text(
        'Hola {}, todo de diez por aca!'.format(update.message.from_user.first_name))


def _operar_dia_wfh(bot, update, prep_message, method):
    try:
        telegram_id = update.message.from_user.id
        username = update.message.from_user.first_name
        days_left = METHODS.get(method)(telegram_id)
        if int(days_left)>0:
            update.message.reply_text(f'{prep_message}. {username} Te quedan {days_left} días de trabajo remoto extras...usalos sabiamente')
        else:
            update.message.reply_text(f'{username} no te quedan más días de trabajo remoto extras :(. Si necesitas más días podés consultarlo con la asamblea')
    except Exception as err:
        update.message.reply_text(f'{username} lo lamentamos pero hubo un error...contactate con al área administrativa')

def listar_dias_wfh(bot, update):
    prep_message = ''
    _operar_dia_wfh(bot, update, prep_message, OBTENER_DIAS_WFH)

def tomar_dia_wfh(bot, update):
    prep_message = 'Día pedido exitosamente.'
    _operar_dia_wfh(bot, update, prep_message, TOMAR_DIA_WFH)

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('micooptest', micoop_test))
updater.dispatcher.add_handler(CommandHandler('tomarwfh', tomar_dia_wfh))
updater.dispatcher.add_handler(CommandHandler('listarwfh', listar_dias_wfh))

updater.start_polling()
updater.idle()
