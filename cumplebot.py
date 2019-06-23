#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
#   Bot programado usando la libreria de pyTelegramBot que se puede encontrar en
#   https://github.com/eternnoir/pyTelegramBotAPI
#

import telebot
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
bot_token = "TOKEN"
from telebot import types
bot = telebot.TeleBot(token=bot_token)

text_messages = {
    'right_user':
        u'Usa esto para acordarte de los cumples porque eres un despistado y usar una agenda es demasiado sencillo',
    'wrong_user':
        u'Hola! Lo siento pero de momento solo mi credor puede usarme'
}
ID = 291461811
first_time = False
scheduler = BackgroundScheduler()
#List with all the posible months
months = { 'enero':01, 'febrero':02, 'marzo':03, 'abril':04, 'mayo':05, 'junio':06,
'julio':07, 'agosto':05, 'septiembre':05, 'octubre':10, 'noviembre':11, 'diciembre':12}
#List with all the posibles days of the month
days = []
days.extend(range(1, 32))

def is_me(user_id):
    return user_id == ID

def search_birthdays():
    date = datetime.date.today()
    #cumples = open("cumples.csv", "r")
    for cumple in open("cumples.csv", "r"):
        cumple = cumple.split(',')                   
        month = cumple[1]
        day = cumple[2][0] + cumple[2][1]
        if (str(date.day) == day and date.month == months.get(month)):
            msg = ("¡Hoy es el cumpleaños de " + cumple[0] + " !")
            bot.send_message(291461811, msg)

        
@bot.message_handler(commands=['start'])
def on_start(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
    else:
        bot.reply_to(message, text_messages['right_user'])
        if not first_time:
            scheduler = BackgroundScheduler()
            scheduler.add_job(search_birthdays, 'interval', days=1)
            scheduler.start()

@bot.message_handler(commands=["nuevo"])
def on_nuevo(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
    else:
        msg = bot.reply_to(message, "Nombre de la persona")
        bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        name = message.text
        cumples = open("cumples.csv", "a")
        cumples.write(name + ",")
        cumples.close()
        markup = types.ReplyKeyboardMarkup(row_width =2)
        for month in months.keys():
            item = types.KeyboardButton(month)
            markup.row(item)
        msg = bot.reply_to(message, 'Mes del cumple ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_month_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_month_step(message):
    try:
        month = message.text
        cumples = open("cumples.csv", "a")
        cumples.write(month + ",")
        cumples.close()
        markup = types.ReplyKeyboardMarkup(row_width =2)
        for day in days:
            item = types.KeyboardButton(day)
            markup.row(item)

        msg = bot.reply_to(message, 'Dia del cumple ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_day_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_day_step(message):
    try:
        day = message.text
        cumples = open("cumples.csv", "a")
        cumples.write(day + "\r\n")
        cumples.close()
        bot.send_message(message.chat.id, 'cuando sea su cumple yo te lo recuerdo')
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

