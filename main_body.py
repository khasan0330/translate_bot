from library.database import db_history_write, db_history_read
from library.keyboards import generate_languages,  LANGUAGES, get_key_from_value

from googletrans import Translator

from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import os
from dotenv import *
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Questions(StatesGroup):
    """Опросник состояний"""
    src = State()
    dst = State()
    text = State()


@dp.message_handler(commands=['start', 'help', 'about', 'history'])
async def command_start(message: Message):
    """Приветствие пользователя"""
    if message.text == '/start':
        await message.answer('здравствуйте, Вас приветствует бот переводчик')
        await start_questions(message)
    elif message.text == '/help':
        await message.answer('Раздел для помощи, в стадии разработки!!!!!!!')
    elif message.text == '/about':
        await message.answer('Данный бот был создан в учебном центре micros \nдля справки @KhasanKarabayev')
    elif message.text == '/history':
        await get_history(message)


async def get_history(message: Message):
    """Для получения истории перевода пользователя"""
    chat_id = message.chat.id
    stories = db_history_read(chat_id)
    for src, dst, original_text, translate_text in stories[:10]:
        await message.answer(f'''
Вы переводили:
С языка: {src} 
На язык: {dst}
Ваш текст: {original_text}
Бот перевел: {translate_text}''')


async def start_questions(message: Message):
    """Тут мы начинаем опрос"""
    await Questions.src.set()
    await message.answer('С какого языка хотите перевести? ',
                         reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=Questions.src)
async def confirm_src_ask_dst(message: Message, state: FSMContext):
    """Реакция на первый вопрос"""
    if message.text in ['/start', '/help', '/about', '/history']:
        await state.finish()
        await command_start(message)
    elif message.text in LANGUAGES.values():
        async with state.proxy() as data:
            data['src'] = message.text

        await Questions.next()
        await message.answer(f'Вы выбрали {message.text}\nВыберите на какой язык перевести',
                             reply_markup=generate_languages())
    else:
        await message.answer("не надо пытаться меня обмануть, просто нажмите кнопку и все",
                             reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=Questions.dst)
async def confirm_dst_ask_text(message: Message, state: FSMContext):
    """Реакция на второй вопрос"""
    if message.text in ['/start', '/help', '/about', '/history']:
        await state.finish()
        await command_start(message)
    elif message.text in LANGUAGES.values():
        async with state.proxy() as data:
            data['dst'] = message.text
        await Questions.next()
        await message.answer(
            f"Начинаем перевод с {data['src']}, на {data['dst']}\nВведите текст, который хотите перевести"
            , reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("не надо пытаться меня обмануть, просто нажмите кнопку и все",
                             reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=Questions.text)
async def confirm_text_translate(message: Message, state: FSMContext):
    """Для принятия переводимого текста"""
    if message.text in ['/start', '/help', '/about', '/history']:
        await state.finish()
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['text'] = message.text
        await text_translation(message, state)


async def text_translation(message: Message, state: FSMContext):
    """Для перевода"""
    async with state.proxy() as data:
        src = data['src']
        dst = data['dst']
        text = data['text']

    translator = Translator()
    finish_text = translator.translate(text=text, src=get_key_from_value(src), dest=get_key_from_value(dst)).text

    chat_id = message.chat.id
    db_history_write(chat_id, src, dst, text, finish_text)

    await message.answer(finish_text)
    await state.finish()
    await start_questions(message)


executor.start_polling(dp)
