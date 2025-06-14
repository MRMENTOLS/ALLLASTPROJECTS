from telegram.ext import Updater
from handlers import register_handlers
from services.ai_service import init_ai
from config import Config

from services.db_service import init_db

def main():
    print("🚀 Запуск бота...")
    updater = Updater(Config.BOT_TOKEN)

    print("🧠 Подключение к модели ИИ...")
    init_ai()

    print("⚙️ Инициализация базы данных...")
    init_db()

    print("⚙️ Регистрация обработчиков...")
    register_handlers(updater.dispatcher)

    print("✅ Бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()