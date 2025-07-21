import telebot
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я гадалка. Задай мне свой вопрос...")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, f"Ты спросил: {message.text}\nОтвет скрыт... но скоро проявится.")

bot.polling(none_stop=True)