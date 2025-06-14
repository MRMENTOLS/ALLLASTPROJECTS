from telebot import TeleBot
from keyboards.reply import get_main_keyboard, get_faq_keyboard, get_department_keyboard

FAQ = {
    "🛒 Как оформить заказ?": "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку «Добавить в корзину», затем перейдите в корзину и следуйте инструкциям для завершения покупки.",
    
    "📦 Как узнать статус заказа?": "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел «Мои заказы». Там будет указан текущий статус вашего заказа.",
    
    "❌ Как отменить заказ?": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.",
    
    "⚠️ Что делать, если товар пришёл повреждённым?": "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.",
    
    "💬 Как связаться с техподдержкой?": "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.",
    
    "🚚 Как узнать информацию о доставке?": "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."
}

def handle_start(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            "👋 Привет! Я бот техподдержки магазина «Продаём всё на свете».\n\n"
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
    def go_back(message):
        bot.send_message(
            message.chat.id,
            "🏠 Вы вернулись в главное меню.",
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(func=lambda m: m.text in FAQ.keys())
    def send_faq_answer(message):
        bot.send_message(message.chat.id, FAQ[message.text], reply_markup=get_faq_keyboard())

    @bot.message_handler(func=lambda m: m.text == "❓ Часто задаваемые вопросы")
    def show_faq(message):
        bot.send_message(
            message.chat.id,
            "❓ Выберите вопрос из списка ниже:",
            reply_markup=get_faq_keyboard()
        )

    @bot.message_handler(func=lambda m: m.text == "📞 Написать в поддержку")
    def choose_department(message):
        bot.send_message(
            message.chat.id,
            "📬 Выберите, в какой отдел вы хотите обратиться:",
            reply_markup=get_department_keyboard()
        )