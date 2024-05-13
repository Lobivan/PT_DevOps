import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater, CommandHandler

import search_info
import validation
import linux_monitoring
import db_commands

logging.basicConfig(
    level=logging.DEBUG, filename='logfile.txt', encoding="utf-8", filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# logger = logging.getLogger(__name__)

logging.debug('Получение токена бота')
load_dotenv()
TOKEN = os.getenv('TOKEN')
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

    # Мониторинг Linux-системы
    dp.add_handler(CommandHandler('get_release', linux_monitoring.getReleaseCommand))
    dp.add_handler(CommandHandler('get_uname', linux_monitoring.getUnameCommand))
    dp.add_handler(CommandHandler('get_uptime', linux_monitoring.getUptimeCommand))
    dp.add_handler(CommandHandler('get_df', linux_monitoring.getDfCommand))
    dp.add_handler(CommandHandler('get_free', linux_monitoring.getFreeCommand))
    dp.add_handler(CommandHandler('get_mpstat', linux_monitoring.getMpstatCommand))
    dp.add_handler(CommandHandler('get_w', linux_monitoring.getWCommand))
    dp.add_handler(CommandHandler('get_auths', linux_monitoring.getAuthsCommand))
    dp.add_handler(CommandHandler('get_critical', linux_monitoring.getCriticalCommand))
    dp.add_handler(CommandHandler('get_ps', linux_monitoring.getPsCommand))
    dp.add_handler(CommandHandler('get_ss', linux_monitoring.getSsCommand))
    dp.add_handler(CommandHandler('get_repl_logs', linux_monitoring.getReplLogsCommand))
    dp.add_handler(CommandHandler('get_services', linux_monitoring.getServicesCommand))
    
    convHandlerAptList = linux_monitoring.getAptListHandler()
    dp.add_handler(convHandlerAptList)

    # Работа с БД
    dp.add_handler(CommandHandler('get_emails', db_commands.getEmailsCommand))
    dp.add_handler(CommandHandler('get_phone_numbers', db_commands.getPhonesCommand))

    


    updater.start_polling()
    updater.idle()
    logging.debug('Остановка бота')

if __name__ == '__main__':
    main()
