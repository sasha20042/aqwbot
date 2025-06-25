import telebot
from telebot import types
import os

API_TOKEN = '8005137384:AAEhT6g4lriKXeFo85Rnly3cP6firNx13pc'
CHAT_ID = '-4870583716'

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📋 Заповнити анкету")
    bot.send_message(message.chat.id, "Привіт! 👋\nНатисни кнопку нижче, щоб заповнити коротку анкету:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📋 Заповнити анкету")
def start_application(message):
    bot.send_message(message.chat.id, "Як тебе звати?", reply_markup=types.ReplyKeyboardRemove())
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Введи номер телефону:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "З якого ти міста?")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    user_data[message.chat.id]['city'] = message.text
    bot.send_message(message.chat.id, "Скільки людей хоче працювати?")
    bot.register_next_step_handler(message, get_people_count)

def get_people_count(message):
    user_data[message.chat.id]['count'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Фабрика багетів (Сладковічово)", "Склад одягу (Угорщина)", "Інше")
    bot.send_message(message.chat.id, "Оберіть вакансію:", reply_markup=markup)
    bot.register_next_step_handler(message, get_position)

def get_position(message):
    user_data[message.chat.id]['position'] = message.text
    text = (
        f"\n📝 Нова заявка:\n\n"
        f"👤 Ім’я: {user_data[message.chat.id]['name']}\n"
        f"📞 Телефон: {user_data[message.chat.id]['phone']}\n"
        f"🏙️ Місто: {user_data[message.chat.id]['city']}\n"
        f"👥 Кількість людей: {user_data[message.chat.id]['count']}\n"
        f"📌 Вакансія: {user_data[message.chat.id]['position']}"
    )
    bot.send_message(CHAT_ID, text)
    bot.send_message(message.chat.id, "✅ Дякуємо! Вашу заявку прийнято. Очікуйте дзвінка!", reply_markup=types.ReplyKeyboardRemove())

print("Бот запущено")
bot.polling(none_stop=True)
