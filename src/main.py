import os
from dotenv import load_dotenv
import logging
import re
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(
    level=logging.DEBUG, filename='logfile.txt', encoding="utf-8", filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# logger = logging.getLogger(__name__)

logging.debug('Получение токена бота')
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
logging.debug('Токен получен: '+ TOKEN[:5] + '...' + TOKEN[-5:])

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

def main():
    logging.debug('Запуск бота')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Поиск электронной почты
    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindEmail)

    # Поиск номеров телефонов
    convHandlerFindPhoneNumber = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumberCommand)],
        states={
            'findPhoneNumber': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumber)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindPhoneNumber)

    updater.start_polling()
    updater.idle()
    logging.debug('Остановка бота')

if __name__ == '__main__':
    main()
