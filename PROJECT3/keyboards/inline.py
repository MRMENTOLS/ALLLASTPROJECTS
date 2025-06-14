from telegram import InlineKeyboardButton, InlineKeyboardMarkup

SUBJECTS = [
    "Русский язык", "Литература", "Иностранный язык", "Алгебра и начала анализа",
    "Геометрия", "Информатика", "Физика", "Химия", "Биология", "История",
    "Обществознание", "География", "Физкультура", "Основы безопасности и защиты Родины",
    "Разговоры о важном"
]

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Начать тест", callback_data='start_test')],
        [InlineKeyboardButton("Случайная профессия", callback_data='random_profession')]
    ])

def get_subjects_keyboard(context=None):
    if context:
        user_data = context.user_data.setdefault("subjects", [])
    else:
        user_data = []

    buttons = []
    for i, s in enumerate(SUBJECTS):
        if s in user_data:
            buttons.append([InlineKeyboardButton(f"✅ {s}", callback_data=f"subject_{i}")])
        else:
            buttons.append([InlineKeyboardButton(s, callback_data=f"subject_{i}")])
    buttons.append([InlineKeyboardButton("✅ Готово", callback_data="finish")])
    return InlineKeyboardMarkup(buttons)