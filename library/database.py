import psycopg2
import os
from dotenv import *
load_dotenv()


def db_connect():
    database = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        host=os.getenv('DB_ADDRESS'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )

    return database


def create_table():
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translate_history(
            history_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            telegram_id BIGINT,
            src VARCHAR(30),
            dst VARCHAR(30),
            original_text VARCHAR(100),
            translate_text VARCHAR(100)
        )
    ''')
    database.commit()
    database.close()


create_table()


def db_history_write(telegram_id, src, dst, original_text, translate_text):
    """Функция для записи истории переводов пользователя"""
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO translate_history(telegram_id, src, dst, original_text, translate_text)
    VALUES (%s, %s, %s, %s, %s)
    ''', (telegram_id, src, dst, original_text, translate_text))
    database.commit()
    database.close()


def db_history_read(telegram_id):
    """Функция для чтения истории переводов пользователя"""
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT src, dst, original_text, translate_text FROM translate_history
    WHERE telegram_id = %s;
    ''', (telegram_id,))
    history = cursor.fetchall()
    history = history[::-1]
    database.close()
    return history
