from telegram import Update
import logging
import re
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import db_commands

ADD_PHONE_NUMBER = range(1)
ADD_EMAIL = range(1)

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
    context.user_data['pnList'] = phoneNumberList
    update.message.reply_text('Введите \'Да\' для записи номеров в базу данных')
    logging.debug('Поиск номеров закончился')
    return ADD_PHONE_NUMBER

def addPhoneNumber(update: Update, context):
    logging.debug('Добавление телефонов в базу данных началось')
    user_input = update.message.text
    if (user_input == 'Да'):
        phoneNumberList = context.user_data['pnList']

        command = 'insert into phones (number) values '
        for i in range(len(phoneNumberList)):
            command += "('" + phoneNumberList[i] + "'), "
        command = command[:-2] + ';'

        data = db_commands.runQueryNoOutput(command)
        update.message.reply_text('Результат - ' + data)
    else:
        update.message.reply_text('Номера НЕ записаны в базу данных')

    logging.debug('Добавление телефонов в базу данных закончилось')
    return ConversationHandler.END

def getPhoneNumberHandler(command = 'find_phone_number'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, findPhoneNumberCommand)],
        states={
            'findPhoneNumber': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumber)],
            ADD_PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, addPhoneNumber)],
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
    context.user_data['eList'] = emailList
    update.message.reply_text('Введите \'Да\' для записи адресов в базу данных')
    logging.debug('Поиск почты закончился')
    return ADD_EMAIL

def addEmail(update: Update, context):
    logging.debug('Добавление адресов в базу данных началось')
    user_input = update.message.text
    if (user_input == 'Да'):
        emailList = context.user_data['eList']

        command = 'insert into email (address) values '
        for i in range(len(emailList)):
            command += "('" + emailList[i] + "'), "
        command = command[:-2] + ';'

        data = db_commands.runQueryNoOutput(command)
        update.message.reply_text('Результат - ' + data)
    else:
        update.message.reply_text('Адресоа НЕ записаны в базу данных')

    logging.debug('Добавление адресов в базу данных закончилось')
    return ConversationHandler.END

def getEmailHandler(command = 'find_email'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
            ADD_EMAIL: [MessageHandler(Filters.text & ~Filters.command, addEmail)],
        },
        fallbacks=[]
    )
