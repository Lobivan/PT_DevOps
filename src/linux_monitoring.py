import paramiko
import os
import re
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def execCommand(comand):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(comand)
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    return data

def getReleaseCommand(update: Update, context):
    logging.debug('Сбор информации о релизе начался')
    data = execCommand('cat /etc/os-release')
    update.message.reply_text(data)
    logging.debug('Сбор информации о релизе закончился')

def getUnameCommand(update: Update, context):
    logging.debug('Сбор информации об архитектуре процессора, имени хоста системы и версии ядра начался')
    data = execCommand('uname -p && uname -n && uname -v')
    update.message.reply_text(data)
    logging.debug('Сбор информации об архитектуре процессора, имени хоста системы и версии ядра закончился')

def getUptimeCommand(update: Update, context):
    logging.debug('Сбор информации о времени работы начался')
    data = execCommand('uptime')
    update.message.reply_text(data)
    logging.debug('Сбор информации о времени работы закончился')

def getDfCommand(update: Update, context):
    logging.debug('Сбор информации состоянии файловой системы начался')
    data = execCommand('df -h')
    update.message.reply_text(data)
    logging.debug('Сбор информации о состоянии файловой системы закончился')

def getFreeCommand(update: Update, context):
    logging.debug('Сбор информации о состоянии оперативной памяти начался')
    data = execCommand('free -h')
    update.message.reply_text(data)
    logging.debug('Сбор информации о состоянии оперативной памяти закончился')

def getMpstatCommand(update: Update, context):
    logging.debug('Сбор информации о производительности системы начался')
    data = execCommand('mpstat')
    update.message.reply_text(data)
    logging.debug('Сбор информации о производительности системы закончился')

def getWCommand(update: Update, context):
    logging.debug('Сбор информации о работающих в данной системе пользователях начался')
    data = execCommand('w')
    update.message.reply_text(data)
    logging.debug('Сбор информации о работающих в данной системе пользователях закончился')

def getAuthsCommand(update: Update, context):
    logging.debug('Сбор логов Последние 10 входов в систему начался')
    data = execCommand('last | grep -v "reboot" | head -n10')
    update.message.reply_text(data)
    logging.debug('Сбор логов Последние 10 входов в систему закончился')

def getCriticalCommand(update: Update, context):
    logging.debug('Сбор логов Последние 5 критических события начался')
    data = execCommand('journalctl -p 2 -r -n5')
    update.message.reply_text(data)
    logging.debug('Сбор логов Последние 5 критических события закончился')

def getPsCommand(update: Update, context):
    logging.debug('Сбор информации о запущенных процессах начался')
    data = execCommand('ps -e')
    update.message.reply_text(data)
    logging.debug('Сбор информации о запущенных процессах закончился')

def getSsCommand(update: Update, context):
    logging.debug('Сбор информации об используемых порта начался')
    data = execCommand('ss')
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x+4096])
    else:
        update.message.reply_text(data)
    logging.debug('Сбор информации об используемых портах закончился')

def aptListCommand(update: Update, context):
    logging.debug('Получена команда сбора информации об установленных пакетах')
    update.message.reply_text('Введите \"все\" для вывода всех пакетов, или название пакета для поиска: ')
    return 'aptList'

def aptList (update: Update, context):
    logging.debug('Сбор информации об установленных пакетах начался')
    user_input = update.message.text

    if user_input == 'все':
        data = execCommand('apt list --installed')
    else:
        data = execCommand('apt list --installed | grep \"' + user_input + '\"')

    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x+4096])
    else:
        update.message.reply_text(data)
    logging.debug('Сбор информации об установленных пакетах начался')
    return ConversationHandler.END

def getAptListHandler(command = 'get_apt_list'):
    return ConversationHandler(
        entry_points=[CommandHandler(command, aptListCommand)],
        states={
            'aptList': [MessageHandler(Filters.text & ~Filters.command, aptList)],
        },
        fallbacks=[]
    )

def getServicesCommand(update: Update, context):
    logging.debug('Сбор информации о запущенных сервисах начался')
    data = execCommand('service --status-all | grep \'\\[ + \\]\'')
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x+4096])
    else:
        update.message.reply_text(data)
    logging.debug('Сбор информации о запущенных сервисах закончился')
