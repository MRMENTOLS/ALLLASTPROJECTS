import telebot
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.admin import handle_admin
from handlers.callbacks import handle_callbacks

import config

bot = telebot.TeleBot(config.BOT_TOKEN)

# Регистрируем хендлеры
handle_start(bot)
handle_help(bot)
handle_admin(bot)
handle_callbacks(bot)

print("Бот запущен...")
bot.polling(none_stop=True)