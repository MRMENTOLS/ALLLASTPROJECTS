from telebot import TeleBot
from keyboards.inline import get_welcome_keyboard
import config
import os
def handle_start(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            "👋 Привет! Я бот онлайн-школы. Нажми на кнопку ниже, чтобы получить расписание уроков.\n\n"
            "💡 Для справки используйте команду /help.",
            reply_markup=get_welcome_keyboard()
        )

    @bot.message_handler(commands=['download_schedule'])
    def send_schedule_file(message):
        if os.path.exists(config.SCHEDULE_PHOTO_PATH):
            with open(config.SCHEDULE_PHOTO_PATH, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="📅 Расписание на неделю")

        if os.path.exists(config.SCHEDULE_FILE_PATH):
            with open(config.SCHEDULE_FILE_PATH, 'rb') as doc:
                bot.send_document(message.chat.id, doc, caption="📎 Полный файл расписания")