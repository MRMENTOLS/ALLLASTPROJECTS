from telebot import TeleBot
from keyboards.reply import get_admin_keyboard
import config
import os

# Состояния пользователя
ADMIN_MENU, EDIT_SCHEDULE, ADD_ANNOUNCEMENT, ADD_ADMIN, UPLOAD_PHOTO, UPLOAD_FILE = range(6)
user_states = {}  # {user_id: state}


def handle_admin(bot: TeleBot):
    @bot.message_handler(commands=['admin'])
    def admin_menu(message):
        if message.from_user.id not in config.ADMINS:
            bot.reply_to(message, "❌ У вас нет прав для доступа к админ-панели.")
            return

        user_states[message.from_user.id] = ADMIN_MENU
        bot.send_message(
            message.chat.id,
            "🔐 Добро пожаловать в админ-панель!",
            reply_markup=get_admin_keyboard()
        )

    @bot.message_handler(func=lambda m: m.text == "⏰ Изменить расписание")
    def set_schedule_prompt(message):
        if message.from_user.id not in config.ADMINS:
            return
        user_states[message.from_user.id] = EDIT_SCHEDULE
        bot.send_message(
            message.chat.id,
            "✍️ Отправьте новое расписание в формате:\n\nПонедельник: Предмет (время)\nВторник: ...\n...",
            reply_markup=None
        )

    @bot.message_handler(func=lambda m: m.text == "📢 Добавить объявление")
    def add_announcement_prompt(message):
        if message.from_user.id not in config.ADMINS:
            return
        user_states[message.from_user.id] = ADD_ANNOUNCEMENT
        bot.send_message(
            message.chat.id,
            "✍️ Напишите текст объявления для добавления:",
            reply_markup=None
        )

    @bot.message_handler(func=lambda m: m.text == "➕ Назначить админа")
    def prompt_new_admin(message):
        if message.from_user.id != config.MAIN_ADMIN_ID:
            return
        user_states[message.from_user.id] = ADD_ADMIN
        bot.send_message(
            message.chat.id,
            "✍️ Отправьте Telegram ID нового администратора.",
            reply_markup=None
        )

    @bot.message_handler(func=lambda m: m.text == "📤 Загрузить файл/фото")
    def upload_file_prompt(message):
        if message.from_user.id not in config.ADMINS:
            return
        user_states[message.from_user.id] = UPLOAD_PHOTO
        bot.send_message(
            message.chat.id,
            "📷 Отправьте фото с расписанием",
            reply_markup=None
        )

    @bot.message_handler(content_types=['photo'], func=lambda m: user_states.get(m.from_user.id) == UPLOAD_PHOTO)
    def handle_uploaded_photo(message):
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(config.SCHEDULE_PHOTO_PATH, 'wb') as new_file:
                new_file.write(downloaded_file)

            user_states[message.from_user.id] = UPLOAD_FILE
            bot.send_message(message.chat.id, "📄 Теперь отправьте файл с расписанием (PDF, Word и т.п.)")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при загрузке фото: {e}")
            bot.send_message(message.chat.id, "📦 Вернитесь в меню:", reply_markup=get_admin_keyboard())

    @bot.message_handler(content_types=['document'], func=lambda m: user_states.get(m.from_user.id) in [UPLOAD_PHOTO, UPLOAD_FILE])
    def handle_uploaded_file(message):
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            file_name = message.document.file_name
            file_path = config.SCHEDULE_FILE_PATH  # Сохраняем как .pdf (можно сохранять с оригинальным именем)

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, "✅ Фото и файл с расписанием успешно загружены!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при загрузке файла: {e}")
        finally:
            bot.send_message(message.chat.id, "📦 Вернитесь в меню:", reply_markup=get_admin_keyboard())

    @bot.message_handler(func=lambda m: m.from_user.id in config.ADMINS and m.text not in ["⏰ Изменить расписание", "📢 Добавить объявление", "➕ Назначить админа", "📤 Загрузить файл/фото"])
    def process_admin_input(message):
        user_id = message.from_user.id
        state = user_states.get(user_id)

        if state == EDIT_SCHEDULE:
            try:
                new_schedule = {}
                lines = message.text.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        day, lesson = line.split(':', 1)
                        new_schedule[day.strip()] = lesson.strip()
                config.DEFAULT_SCHEDULE = new_schedule
                config.data["schedule"] = new_schedule
                config.save_data(config.data)
                bot.send_message(message.chat.id, "✅ Расписание успешно обновлено и сохранено!")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Ошибка при обновлении расписания: {e}")
            finally:
                bot.send_message(message.chat.id, "📦 Теперь вы можете:", reply_markup=get_admin_keyboard())

        elif state == ADD_ANNOUNCEMENT:
            announcement_text = message.text.strip()
            config.ANNOUNCEMENTS.append(announcement_text)
            config.data["announcements"] = config.ANNOUNCEMENTS
            config.save_data(config.data)
            bot.send_message(message.chat.id, "✅ Объявление успешно добавлено и сохранено.")
            bot.send_message(message.chat.id, "📦 Теперь вы можете:", reply_markup=get_admin_keyboard())

        elif state == ADD_ADMIN:
            if user_id != config.MAIN_ADMIN_ID:
                bot.send_message(message.chat.id, "❌ Только главный админ может назначать новых админов.")
                bot.send_message(message.chat.id, "📦 Теперь вы можете:", reply_markup=get_admin_keyboard())
                return

            try:
                new_admin_id = int(message.text.strip())
                if new_admin_id not in config.ADMINS:
                    config.ADMINS.append(new_admin_id)
                    config.data["admins"] = config.ADMINS
                    config.save_data(config.data)
                    bot.send_message(message.chat.id, f"✅ Пользователь с ID {new_admin_id} назначен админом.")
                else:
                    bot.send_message(message.chat.id, "⚠️ Этот пользователь уже является админом.")
            except ValueError:
                bot.send_message(message.chat.id, "❌ Неверный формат ID. Введите число.")
            finally:
                bot.send_message(message.chat.id, "📦 Теперь вы можете:", reply_markup=get_admin_keyboard())

        else:
            bot.send_message(message.chat.id, "📦 Вы вернулись в главное меню.", reply_markup=get_admin_keyboard())