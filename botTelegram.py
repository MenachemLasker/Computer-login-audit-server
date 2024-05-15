import telebot
import os
import json
from usersManger import *
from telegram import *
from typing import final
BOT_TOKEN = '6906120319:AAGcdv8JCg5zjWgksXk7pCNm-VfqPP3mw7Q'
bot = telebot.TeleBot(BOT_TOKEN)



@bot.message_handler(commands=['follow'])
def handle_follow(message):
    msg = bot.reply_to(message, "אנא הזן שם משתמש:")
    bot.register_next_step_handler(msg, get_username_step)

def get_username_step(message):
    chat_id = message.chat.id
    username = message.text
    if has_user(username):
        msg = bot.reply_to(message, "אנא הזן סיסמה:")
        bot.register_next_step_handler(msg, password_step, username)
    else:
        msg = bot.reply_to(message, "שם המשתמש לא קיים, אנא נסה שוב:")
        bot.register_next_step_handler(msg, get_username_step)

def password_step(message, username):
    chat_id = message.chat.id
    password = message.text
    if verify_user(username, password):
        follow_user(username, chat_id)
        bot.send_message(chat_id, "עקבת אחרי המשתמש בהצלחה.")
    else:
        bot.send_message(chat_id, "err")

@bot.message_handler(commands=['unfollow'])
def handle_unfollow(message):
    msg = bot.reply_to(message, "אנא הזן שם משתמש:")
    bot.register_next_step_handler(msg, un)


def has_followrs(username):
    file_path = ('user_chat_ids.json')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as infile:
            user_chat_ids = json.load(infile)
            return user_chat_ids.get(username)
    return False


def save_user_chat_id(username, chat_id):
    file_path = ('user_chat_ids.json')
    if not has_followrs(username):
        new_user_chat_ids = {
            username: [chat_id]
        }
        if os.path.isfile(file_path):
            with open(file_path, 'r') as infile:
                user_chat_ids = json.load(infile)
            user_chat_ids.update(user_chat_ids)
        else:
            user_chat_ids = new_user_chat_ids
    else:
        with open(file_path, 'r') as infile:
            user_chat_ids = json.load(infile)
            user_chat_ids(username).append(chat_id)
    with open(file_path, 'w') as outfile:
        json.dump(user_chat_ids, outfile)
    print(f"Data added to {file_path}")

def remove_user_chat_id(username, chat_id):
    file_path = ('user_chat_ids.json')
    if not has_followrs(username):
        return False
    else:
        with open(file_path, 'r') as infile:
            user_chat_ids = json.load(infile)
            user_chat_ids(username).remove(chat_id)
        with open(file_path, 'w') as outfile:
            json.dump(user_chat_ids, outfile)
        return True

def get_user_chat_id(username):
    with open('user_chat_ids.json', 'r') as file:
        user_chat_ids = json.load(file)
        user_chat_id = user_chat_ids[username]
        return user_chat_id


def follow_user(username,chat_id):
    save_user_chat_id(username, chat_id)
    bot.send_message(chat_id, f"אתה עכשיו עוקב אחרי {username}.")
def unfollow_user(username,chat_id):
    remove_user_chat_id(username, chat_id)
    bot.send_message(chat_id, f"אתה עכשיו לא עוקב אחרי {username}.")

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "/follow")


def get_ids(username):
    with open('user_chat_ids.json', 'r') as file:
        user_chat_ids = json.load(file)
        list_chat_id = user_chat_ids[username]
        return list_chat_id

def start_bot():
    bot.polling()
