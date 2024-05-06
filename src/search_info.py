from telegram import Update, ForceReply
import logging
import re
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

# Поиск номеров телефонов
def findPhoneNumberCommand(update: Update, context):
    logging.debug('Получена команда поиска номеров')
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'findPhoneNumber'

def findPhoneNumber (update: Update, context):
    logging.debug('Поиск номеров начался')
    user_input = update.message.text
    phoneNumRegex = re.compile(r'(?:\+7|8)(?: \(\d{3}\) \d{3}-\d{2}-\d{2}|\d{10}|\(\d{3}\)\d{7}| \d{3} \d{3} \d{2} \d{2}| \(\d{3}\) \d{3} \d{2} \d{2}|-\d{3}-\d{3}-\d{2}-\d{2}|\(\d{3}\)\d{3}-\d{2}-\d{2}|\(\d{3}\)\d{3} \d{2} \d{2})')
    phoneNumberList = phoneNumRegex.findall(user_input)
    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        return
    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' 
    update.message.reply_text(phoneNumbers)
    logging.debug('Поиск номеров закончился')
    return ConversationHandler.END

def getPhoneNumberHandler(command = 'find_phone_number'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, findPhoneNumberCommand)],
        states={
            'findPhoneNumber': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumber)],
        },
        fallbacks=[]
    )


# Поиск электронной почты
def findEmailCommand(update: Update, context):
    logging.debug('Получена команда поиска почты')
    update.message.reply_text('Введите текст для поиска электронной почты: ')
    return 'findEmail'

def findEmail (update: Update, context):
    logging.debug('Поиск почты начался')
    user_input = update.message.text
    emailRegex = re.compile(r'[\w]+[\w\-\.]+[a-zA-z0-9]+@(?:[\w-]+\.)+[\w-]+')
    emailList = emailRegex.findall(user_input)
    if not emailList:
        update.message.reply_text('Электронная почта не найдена')
        return
    email = ''
    for i in range(len(emailList)):
        email += f'{i+1}. {emailList[i]}\n' 
    update.message.reply_text(email)
    logging.debug('Поиск почты закончился')
    return ConversationHandler.END

def getEmailHandler(command = 'find_email'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
        },
        fallbacks=[]
    )
