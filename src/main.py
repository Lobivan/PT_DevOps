import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater

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
    convHandlerValidatePass = validation.getHandler()
    dp.add_handler(convHandlerValidatePass)

    # Поиск электронной почты
    convHandlerFindEmail = search_info.getEmailHandler()
    dp.add_handler(convHandlerFindEmail)

    # Поиск номеров телефонов
    convHandlerFindPhoneNumber = search_info.getPhoneNumberHandler()
    dp.add_handler(convHandlerFindPhoneNumber)

    updater.start_polling()
    updater.idle()
    logging.debug('Остановка бота')

if __name__ == '__main__':
    main()
