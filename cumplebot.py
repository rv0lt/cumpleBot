#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
#   Bot programado usando la libreria de pyTelegramBot que se puede encontrar en
#   https://github.com/eternnoir/pyTelegramBotAPI
import time
import telebot
import datetime
import csv
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

bot_token = "791676020:AAGci5a5u4wGylHgQGtOtzCMzB45kU-mJZQ"
bot = telebot.TeleBot(token=bot_token)
text_messages = {
    'right_user':
        'Usa esto para acordarte de los cumples porque eres un despistado y usar una agenda es demasiado sencillo',
    'wrong_user':
        'Hola! Lo siento pero de momento solo mi credor puede usarme'
}
ID = 291461811
first_time = False
scheduler = BackgroundScheduler()
#List with all the posible months
months = { 'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6,
'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
#List with all the posibles days of the month
days = []
days.extend(range(1, 32))
commands=[
    'start',
    'nuevo',
    'borrar',
    'mostrar'
]
def is_me(user_id):
    return user_id == ID

def search_birthdays():
    date = datetime.date.today()
    print("aaa")
    for cumple in open("cumples.csv", "r"):
        cumple = cumple.split(',')                   
        day = cumple[1]
        month = cumple[2]
        month = month.split("\r\n")[0]
        print(day + " " + month)
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
            scheduler.add_job(search_birthdays, 'interval', seconds=4)
            scheduler.start()

@bot.message_handler(commands=['borrar'])
def on_delete(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
        return
    msg = bot.reply_to(message, "¿De quien quierres borrar su cumpleaños?") 
    bot.register_next_step_handler(msg, process_delete)

def process_delete(message):  
    remove_word = message.text 
    with open("cumples.csv", "r") as f:
        lines = f.readlines()
    with open("cumples.csv", "w") as f:
        for line in lines:
            aux = line.split(',')
            if not remove_word == aux[0]:
                f.write(line)

@bot.message_handler(commands=["mostrar"])
def on_mostrar(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, text_messages['wrong_user'])
    else:
        with open("cumples.csv", "r") as f:
            lines = f.readlines()
            msg = ""
            for cumple in lines:
                msg = msg + cumple + "\r\n"
            bot.reply_to(message, msg)

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
        cumples=open("cumples.csv", "a")
        cumples.write(day + ",")
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
        cumples=open("cumples.csv", "a")
        cumples.write(month + "\r\n")
        cumples.close
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

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(10)

