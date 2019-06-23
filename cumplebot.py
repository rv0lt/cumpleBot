#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
#   Bot programado usando la libreria de pyTelegramBot que se puede encontrar en
#   https://github.com/eternnoir/pyTelegramBotAPI
#

import telebot
import time
import random
bot_token = "TOKEN"

bot = telebot.TeleBot(token=bot_token)

text_messages = {
    'right_user':
        u'Usa esto para acordarte de los cumplea�os porque eres un despistado',
    'wrong_user':
        u'Hola! Lo siento pero de momento solo mi credor puede usarme'
}
ID = 291461811
class User:
    def __init__(self, name):
        self.name = name
        self.date = None

def is_me(user_id):
    return user_id == ID

@bot.message_handler(commands=['start'])
def on_start(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
    else:
        bot.reply_to(message, text_messages['right_user'])

@bot.message_handler(commands=["nuevo"])
def on_nuevo(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
    else:
        file1 = open("cumples.csv", "a")
        msg = bot.reply_to(message, "Nombre de la persona")
        bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        name = message.text
        file1 = open("cumples.csv", "a")
        file1.write(name + ",")
        file1.close()
        bot.send_message(message.chat.id, name)
        msg = bot.reply_to(message, 'Dia del cumple(formato DD/MM)')
        bot.register_next_step_handler(msg, process_date_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_date_step(message):
    try:

        date = message.text
        file1 = open("cumples.csv", "a")
        file1.write(date + "\r\n")
        file1.close()
        bot.send_message(message.chat.id, date)
    except Exception as e:
        bot.reply_to(message, 'oooops')



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")


bot.polling()