from telebot import TeleBot
from keyboards.reply import get_department_keyboard
from services.db_service import save_ticket
from keyboards.reply import get_main_keyboard
import config

def handle_callbacks(bot: TeleBot):
    @bot.message_handler(func=lambda m: m.text in ["💻 Программисты", "💰 Отдел продаж"])
    def forward_to_support(message):
        department = message.text
        msg = bot.send_message(
            message.chat.id,
            f"✍️ Напишите ваш вопрос для {department}.",
            reply_markup=None
        )
        bot.register_next_step_handler(msg, lambda m: save_and_confirm(m, department))

    def save_and_confirm(message, department):
        user = message.from_user
        full_name = user.full_name
        question = message.text.strip()

        save_ticket(user.id, full_name, question, department)

        bot.send_message(
            message.chat.id,
            "✅ Ваше сообщение передано в техподдержку. С вами свяжутся в ближайшее время!",
            reply_markup=get_main_keyboard()
        )