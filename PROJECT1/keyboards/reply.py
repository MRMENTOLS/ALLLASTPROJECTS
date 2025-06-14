from telebot.types import ReplyKeyboardMarkup

def get_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⏰ Изменить расписание")
    markup.add("📢 Добавить объявление")
    markup.add("➕ Назначить админа")
    markup.add("📤 Загрузить файл/фото")
    return markup