from telegram import Update
from keyboards.inline import get_start_keyboard

def start(update, context):
    context.user_data.clear()  # Очистка предыдущих данных
    update.message.reply_text(
        "🚀 Привет! Я помогу тебе выбрать карьеру. Выбери действие:",
        reply_markup=get_start_keyboard()
    )