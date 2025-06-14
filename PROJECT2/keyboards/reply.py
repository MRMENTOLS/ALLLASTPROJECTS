from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("❓ Часто задаваемые вопросы"))
    markup.row(KeyboardButton("📞 Написать в поддержку"))
    return markup

def get_faq_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🛒 Как оформить заказ?"))
    markup.row(KeyboardButton("📦 Как узнать статус заказа?"))
    markup.row(KeyboardButton("❌ Как отменить заказ?"))
    markup.row(KeyboardButton("⚠️ Что делать, если товар пришёл повреждённым?"))
    markup.row(KeyboardButton("💬 Как связаться с техподдержкой?"))
    markup.row(KeyboardButton("🚚 Как узнать информацию о доставке?"))
    markup.row(KeyboardButton("⬅️ Назад"))
    return markup

def get_department_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("💻 Программисты"))
    markup.row(KeyboardButton("💰 Отдел продаж"))
    markup.row(KeyboardButton("⬅️ Назад"))
    return markup