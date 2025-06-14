from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_welcome_keyboard():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("📅 Получить расписание", callback_data="get_schedule")
    markup.add(btn)
    return markup

def get_welcome_keyboard():
    markup = InlineKeyboardMarkup()
    schedule_btn = InlineKeyboardButton("📅 Получить расписание", callback_data="get_schedule")
    announcements_btn = InlineKeyboardButton("📢 Посмотреть объявления", callback_data="show_announcements")
    markup.row(schedule_btn)
    markup.row(announcements_btn)
    return markup