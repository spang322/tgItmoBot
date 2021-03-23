# from telebot import types
from config import *

def help(message):
    bot.send_message(message.from_user.id, "Бог поможет")

def noCom(message):
    bot.send_message(message.from_user.id, "Такой команды нет")

def reg(message):
    bot.send_message(message.from_user.id, "Пора зарегистрироваться!\nВведите свой ник")
    bot.register_next_step_handler(message, createProfile)

def createProfile(message):
    db.reg(message.text, message.from_user.id)
    info = db.profileInfo(message.from_user.id)
    bot.send_message(message.from_user.id, f"ID: {info[0]}\nНик: {info[1]}\nДенег: {info[2]}")
