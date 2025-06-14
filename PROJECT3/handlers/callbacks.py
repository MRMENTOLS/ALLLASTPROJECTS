from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# Импорты из других модулей
from services.ai_service import generate_profession_recommendations, parse_ai_response
from services.db_service import add_profession_to_db
from keyboards.inline import SUBJECTS, get_subjects_keyboard


def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.answer()

    if data == 'start_test':
        # Очищаем/инициализируем список предметов
        context.user_data["subjects"] = []
        query.edit_message_text("Выбери свои любимые школьные предметы:")
        query.edit_message_reply_markup(reply_markup=get_subjects_keyboard(context))

    elif data.startswith('subject_'):
        # Обработка выбора предмета
        user_data = context.user_data.setdefault("subjects", [])
        subject_idx = int(data.split('_')[1])
        subject = SUBJECTS[subject_idx]

        if subject in user_data:
            user_data.remove(subject)
        else:
            user_data.append(subject)

        # Обновляем клавиатуру
        buttons = []
        for i, s in enumerate(SUBJECTS):
            if s in user_data:
                buttons.append([InlineKeyboardButton(f"✅ {s}", callback_data=f"subject_{i}")])
            else:
                buttons.append([InlineKeyboardButton(s, callback_data=f"subject_{i}")])
        buttons.append([InlineKeyboardButton("✅ Готово", callback_data="finish")])

        try:
            query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            print(f"❌ Ошибка при обновлении клавиатуры: {e}")

    elif data == 'finish':
        selected = context.user_data.get("subjects", [])
        if not selected:
            query.answer("Вы не выбрали ни один предмет!")
            return

        # Показываем, что бот думает
        query.edit_message_text("🧠 Подбираем профессии, которые подойдут именно вам...")

        # Получаем ответ от ИИ
        raw_response = generate_profession_recommendations(selected)

        if raw_response:
            professions_list = parse_ai_response(raw_response)

            if professions_list:
                for prof in professions_list:
                    add_profession_to_db(prof, selected)
                query.edit_message_text(raw_response)
            else:
                query.edit_message_text("🧠 Не удалось получить рекомендации от ИИ.")
        else:
            from services.db_service import get_random_profession_from_db
            profession = get_random_profession_from_db()
            if profession:
                education_links = '\n  '.join(profession['education'])
                text = (
                    f"📚 Мы не смогли получить ответ от ИИ, но нашли случайную профессию:\n\n"
                    f"💼 *{profession['name']}*\n\n"
                    f"{profession['description']}\n\n"
                    f"💰 Зарплата:\n"
                    f"  - {profession['salary']}\n\n"
                    f"📚 Где учиться:\n"
                    f"  {education_links}"
                )
                query.edit_message_text(text, parse_mode="Markdown")
            else:
                query.edit_message_text("❌ Не удалось получить ответ от ИИ и в БД нет профессий.")


# --- Вспомогательная функция ---
def get_subjects_keyboard(context: CallbackContext):
    user_data = context.user_data.setdefault("subjects", [])

    buttons = []
    for i, s in enumerate(SUBJECTS):
        if s in user_data:
            buttons.append([InlineKeyboardButton(f"✅ {s}", callback_data=f"subject_{i}")])
        else:
            buttons.append([InlineKeyboardButton(s, callback_data=f"subject_{i}")])
    buttons.append([InlineKeyboardButton("✅ Готово", callback_data="finish")])
    return InlineKeyboardMarkup(buttons)