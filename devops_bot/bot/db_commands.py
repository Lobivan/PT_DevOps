from telegram import Update
import logging
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
load_dotenv()

def runQueryWithReturn(query):
    data = ''
    try:
        connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                  password=os.getenv('DB_PASS'),
                                  host=os.getenv('DB_HOST'),
                                  port=os.getenv('DB_PORT1'), 
                                  database=os.getenv('DB_DATABASE'))

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            data = 'Пустой результат'
    except (Exception, Error) as error:
        logging.debug("Ошибка при работе с PostgreSQL", error)
        data = "Ошибка при работе с PostgreSQL"
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            logging.debug("Соединение с PostgreSQL закрыто")
    return data

def runQueryNoOutput(query):
    data = ''
    try:
        connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                  password=os.getenv('DB_PASS'),
                                  host=os.getenv('DB_HOST'),
                                  port=os.getenv('DB_PORT1'), 
                                  database=os.getenv('DB_DATABASE'))

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        data = 'Успех!'
    except (Exception, Error) as error:
        logging.debug("Ошибка при работе с PostgreSQL", error)
        data = "Ошибка при работе с PostgreSQL, запрос не выполнен!"
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            logging.debug("Соединение с PostgreSQL закрыто")
    return data

def getPhonesCommand(update: Update, context):
    logging.debug('Сбор номеров начался')
    data = runQueryWithReturn("select * from phones;")
    res = ''
    for tup in data:
        line = ''
        for item in tup:
            line += str(item) + ' '
        res += line + '\n'
    update.message.reply_text(res)
    logging.debug('Сбор номеров закончился')

def getEmailsCommand(update: Update, context):
    logging.debug('Сбор email-адресов начался')
    data = runQueryWithReturn("select * from email;")
    res = ''
    for tup in data:
        line = ''
        for item in tup:
            line += str(item) + ' '
        res += line + '\n'
    update.message.reply_text(res)
    logging.debug('Сбор email-адресов закончился')
