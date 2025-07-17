import telebot
import os

TOKEN = os.environ.get("7565761796:AAG4SZag_ZLTIxKxICRXhTyBuKwUY-y78yM")
bot = telebot.TeleBot(7565761796:AAG4SZag_ZLTIxKxICRXhTyBuKwUY-y78yM)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я гадалка-бот!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты сказал: {message.text}")

bot.polling()
