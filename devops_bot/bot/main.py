import os
import re
import logging
import paramiko
from telegram.ext import Updater, CommandHandler, Filters, ConversationHandler, CallbackContext, MessageHandler
from telegram import Update
from functools import partial
from dotenv import load_dotenv

import search_info
# import validation
import db_commands

logging.basicConfig(
    level=logging.DEBUG, filename='logfile.txt', encoding="utf-8", filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.debug('Получение токена бота')
load_dotenv()
TOKEN = os.getenv('TOKEN')
logging.debug('Токен получен: '+ TOKEN[:5] + '...' + TOKEN[-5:])





# --------------------------------- Проверка сложности пароля ---------------------------------

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

# --------------------------------- Мониторинг удалённой системы линукс ---------------------------------

rm_host = os.getenv('RM_HOST')
rm_port = os.getenv('RM_PORT')
rm_username = os.getenv('RM_USER')
rm_password = os.getenv('RM_PASSWORD')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def getAptListOnRmHost(update: Update, context: CallbackContext):
    client.connect(hostname=rm_host, username=rm_username, password=rm_password, port=rm_port)
    if len(context.args) > 0:
        stdin, stdout, stderr = client.exec_command('apt list --installed | grep \"' + context.args[0] + '\"')
    else:
        stdin, stdout, stderr = client.exec_command('apt list --installed')
        update.message.reply_text('Для получения информации о конкретных пакетах введите \"/get_apt_list ИМЯ_ПАКЕТА\"')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    for x in range(0, len(data), 4096):
        update.message.reply_text(data[x:x+4096])
    if len(context.args) == 0:
        update.message.reply_text('Для получения информации о конкретных пакетах введите \"/get_apt_list ИМЯ_ПАКЕТА\"')
    return data

def execCommandOnRmHost(update: Update, context, command):
    client.connect(hostname=rm_host, username=rm_username, password=rm_password, port=rm_port)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    for x in range(0, len(data), 4096):
        update.message.reply_text(data[x:x+4096])
    return data

# --------------------------------- main ---------------------------------

def main():
    logging.debug('Запуск бота')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Проверка сложности пароля
    convHandlerValidatePass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerValidatePass)

    # Поиск электронной почты
    convHandlerFindEmail = search_info.getEmailHandler()
    dp.add_handler(convHandlerFindEmail)

    # Поиск номеров телефонов
    convHandlerFindPhoneNumber = search_info.getPhoneNumberHandler()
    dp.add_handler(convHandlerFindPhoneNumber)

    # Мониторинг Linux-системы
    dp.add_handler(CommandHandler('get_release', partial(execCommandOnRmHost, command='cat /etc/os-release')))
    dp.add_handler(CommandHandler('get_uname', partial(execCommandOnRmHost, command='uname -p && uname -n && uname -v')))
    dp.add_handler(CommandHandler('get_uptime', partial(execCommandOnRmHost, command='uptime')))
    dp.add_handler(CommandHandler('get_df', partial(execCommandOnRmHost, command='df -h')))
    dp.add_handler(CommandHandler('get_free', partial(execCommandOnRmHost, command='free -h')))
    dp.add_handler(CommandHandler('get_mpstat', partial(execCommandOnRmHost, command='mpstat')))
    dp.add_handler(CommandHandler('get_w', partial(execCommandOnRmHost, command='w')))
    dp.add_handler(CommandHandler('get_auths', partial(execCommandOnRmHost, command='last | grep -v "reboot" | head -n10')))
    dp.add_handler(CommandHandler('get_critical', partial(execCommandOnRmHost, command='journalctl -p 2 -r -n5')))
    dp.add_handler(CommandHandler('get_ps', partial(execCommandOnRmHost, command='ps -e')))
    dp.add_handler(CommandHandler('get_ss', partial(execCommandOnRmHost, command='ss')))
    dp.add_handler(CommandHandler('get_services', partial(execCommandOnRmHost, command='service --status-all | grep \'\\[ + \\]\'')))
    dp.add_handler(CommandHandler('get_apt_list', getAptListOnRmHost))

    # Работа с БД
    dp.add_handler(CommandHandler('get_repl_logs', db_commands.getReplLogsCommand))
    dp.add_handler(CommandHandler('get_emails', db_commands.getEmailsCommand))
    dp.add_handler(CommandHandler('get_phone_numbers', db_commands.getPhonesCommand))

    
    updater.start_polling()
    updater.idle()
    logging.debug('Остановка бота')

if __name__ == '__main__':
    main()
