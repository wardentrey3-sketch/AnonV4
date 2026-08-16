import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import json
import random







#--------------------------------------------------------------------------
#13.02.2026 v4.0
#26.07.2026 v4.1

#@TreyWardenTest_bot
BOT_TOKEN = "7780824241:AAEfKnFjI5NNAcZHfW9YmwSjGSlCz3ky6PU"
ADMIN_ID = 1846110852

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(BOT_TOKEN)

joke_url = 'https://otvet.imgsmail.ru/download/291414655_c3a3f533f416a0461c7c234b95edeb77.jpg'

joke_url = 'https://letterboxd.com/abctv/'

users_file_path = r"data/users.json"
codes_file_path = r"data/codes.json"
states_file_path = r"data/states.json"
reply_msgs_file_path = r"data/reply_msg.json"
admins_file_path = r"data/admins.json"
history_file_path = r"data/history.json"

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
code_size = 5


MAX_LENGTH = 4000

reply_msgs_limit = 100

default_code = 'gj0dj'

emotions = [
    "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "🩷", "🩵", "🩶",
    "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟",
    "❤️‍🔥", "💌", "🧡", "♥️", "🫶",
    "🥰", "😍"
]

#--------------------------------------------------------------------------

