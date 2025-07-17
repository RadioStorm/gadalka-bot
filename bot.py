from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAY_URL = os.getenv("PAY_URL")  # например: https://yoomoney.ru/to/410014787925914

users_paid = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔮 Получить предсказание", callback_data="get_prediction")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Приветствую. Чтобы узнать послание судьбы, нажми кнопку ниже.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_prediction":
        user_id = query.from_user.id
        if user_id in users_paid:
            await query.edit_message_text(get_prediction(query.from_user.first_name))
        else:
            keyboard = [[InlineKeyboardButton("💳 Оплатить 100₽", url=PAY_URL)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="Чтобы открыть доступ к посланию, сделай дар судьбе — 100₽.\nПосле оплаты нажми /paid.",
                reply_markup=reply_markup,
            )

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users_paid.add(user_id)
    await update.message.reply_text("Дар принят. Теперь ты можешь получить предсказание. Нажми кнопку ещё раз.")

def get_prediction(user_name):
    return f"{user_name}, звезды говорят: сейчас не время для суеты. Внутренний голос ведёт тебя верно. Прислушайся."

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("paid", paid))

    app.run_polling()
