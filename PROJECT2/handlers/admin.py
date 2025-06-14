from telebot import TeleBot
from models.ticket import SessionLocal, Ticket
import config

def handle_admin(bot: TeleBot):
    @bot.message_handler(commands=['admin'])
    def admin_menu(message):
        if message.from_user.id != config.ADMIN_ID:
            bot.reply_to(message, "❌ У вас нет прав администратора.")
            return

        session = SessionLocal()
        tickets = session.query(Ticket).all()
        session.close()

        if not tickets:
            bot.send_message(message.chat.id, "📭 Нет обращений в техподдержку.")
            return

        for t in tickets:
            bot.send_message(
                message.chat.id,
                f"🎫 ID: {t.id}\n"
                f"👤 Пользователь: {t.full_name} ({t.user_id})\n"
                f"🕘 Время: {t.timestamp}\n"
                f"🧾 Вопрос: {t.question}\n"
                f"💼 Отдел: {t.department}"
            )