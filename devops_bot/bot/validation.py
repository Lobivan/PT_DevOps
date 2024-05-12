from telegram import Update
import logging
import re
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

# Проверка сложности пароля
def verifyPasswordCommand(update: Update, context):
    logging.debug('Получена команда проверки сложности пароля')
    update.message.reply_text('Введите пароль: ')
    return 'verifyPassword'

def verifyPassword (update: Update, context):
    logging.debug('Проверка сложности пароля началась')
    user_input = update.message.text
    passRegex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$')
    passStrong = passRegex.findall(user_input)

    if not passStrong:
        update.message.reply_text('Пароль простой')
    else:
        update.message.reply_text('Пароль сложный')

    logging.debug('Проверка сложности пароля закончилась')
    return ConversationHandler.END

def getHandler(command = 'verify_password'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )
