from telebot import TeleBot
import config

def handle_schedule_button(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data == 'get_schedule')
    def send_schedule(call):
        bot.answer_callback_query(call.id)
        schedule_text = "📅 Ваше расписание:\n\n"
        for day, lesson in config.DEFAULT_SCHEDULE.items():
            schedule_text += f"{day}: {lesson}\n"
        bot.send_message(call.message.chat.id, schedule_text)

    @bot.callback_query_handler(func=lambda call: call.data == 'show_announcements')
    def show_announcements(call):
        bot.answer_callback_query(call.id)
        if config.ANNOUNCEMENTS:
            for announcement in config.ANNOUNCEMENTS:
                bot.send_message(call.message.chat.id, announcement)
        else:
            bot.send_message(call.message.chat.id, "🔔 Пока нет активных объявлений.")