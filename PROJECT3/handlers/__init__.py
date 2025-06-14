from telegram.ext import Dispatcher
from telegram.ext import CommandHandler, CallbackQueryHandler

def register_handlers(dp: Dispatcher):
    from handlers.start import start
    from handlers.callbacks import handle_callback

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))