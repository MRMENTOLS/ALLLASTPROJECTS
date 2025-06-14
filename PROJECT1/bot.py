import telebot
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.admin import handle_admin
from handlers.other_handlers import handle_schedule_button
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

# Регистрируем обработчики
handle_start(bot)
handle_help(bot)
handle_admin(bot)
handle_schedule_button(bot)

print("Бот запущен...")
bot.polling(none_stop=True)