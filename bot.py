import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")
YOOMONEY_LINK = os.getenv("YOOMONEY_LINK")

paid_users = {}

def stylize_response(user_name, text):
    return f"{user_name}, звезды говорят:\n\n{text}\n\nПрислушайся к знакам судьбы..."

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты — мистическая гадалка. Говори таинственно, с образами, без прямых ответов. Намекай на астрологию, числа, чувства."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    return response.json()['choices'][0]['message']['content']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Оплатить 100₽", url=YOOMONEY_LINK)],
        [InlineKeyboardButton("Я оплатил, хочу вопрос", callback_data='paid_confirm')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Чтобы получить ответ, сначала оплати 100 рублей.", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'paid_confirm':
        paid_users[user_id] = paid_users.get(user_id, 0) + 1
        await query.answer()
        await query.edit_message_text("Спасибо! Теперь задай свой вопрос.")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    if paid_users.get(user_id, 0) > 0:
        paid_users[user_id] -= 1
        question = update.message.text
        await update.message.reply_text("Связь с духами установлена, ожидай пророчества...")
        answer = ask_openrouter(question)
        styled = stylize_response(user_name, answer)
        await update.message.reply_text(styled)
    else:
        keyboard = [
            [InlineKeyboardButton("Оплатить 100₽", url=YOOMONEY_LINK)],
            [InlineKeyboardButton("Я оплатил, хочу вопрос", callback_data='paid_confirm')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Пожалуйста, сначала оплати 100 рублей, нажав кнопку ниже.", reply_markup=reply_markup)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))

app.run_polling()