import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import search_info
import validation

logging.basicConfig(
    level=logging.DEBUG, filename='logfile.txt', encoding="utf-8", filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# logger = logging.getLogger(__name__)

logging.debug('Получение токена бота')
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
logging.debug('Токен получен: '+ TOKEN[:5] + '...' + TOKEN[-5:])

def main():
    logging.debug('Запуск бота')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Проверка сложности пароля
    convHandlerValidatePass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', validation.verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, validation.verifyPassword)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerValidatePass)

    # Поиск электронной почты
    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', search_info.findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, search_info.findEmail)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindEmail)

    # Поиск номеров телефонов
    convHandlerFindPhoneNumber = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', search_info.findPhoneNumberCommand)],
        states={
            'findPhoneNumber': [MessageHandler(Filters.text & ~Filters.command, search_info.findPhoneNumber)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindPhoneNumber)

    updater.start_polling()
    updater.idle()
    logging.debug('Остановка бота')

if __name__ == '__main__':
    main()
