from telebot import TeleBot

def handle_help(bot: TeleBot):
    @bot.message_handler(commands=['help'])
    def help_command(message):
        text = (
            "📚 Доступные команды:\n"
            "/start — начать взаимодействие\n"
            "/help — посмотреть справку\n\n"

            "📌 Возможности:\n"
            "- Получать ответы на часто задаваемые вопросы\n"
            "- Задавать свой вопрос специалисту\n"
            "- Выбирать, в какой отдел обращаться\n"
            "- Узнавать статус заказа и другую информацию\n\n"

            "Если возникнут вопросы — пишите в поддержку!"
        )
        bot.reply_to(message, text)