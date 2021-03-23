# from telebot import types
from config import *

def help(message):
    bot.send_message(message.from_user.id, "Вот список команд:\nПрофиль")

def noCom(message):
    bot.send_message(message.from_user.id, "Такой команды нет")

def reg(message):
    bot.send_message(message.from_user.id, "Пора зарегистрироваться!\nВведите свой ник")
    bot.register_next_step_handler(message, createProfile)

def createProfile(message):
    db.reg(message.text, message.from_user.id)
    bot.register_next_step_handler(message, profileInfo)

def profileInfo(message):
    info = db.profileInfoSQL(message.from_user.id)
    bot.send_message(message.from_user.id, f"ID: {info[0]}\nНик: {info[1]}\nДенег: {info[2]}")

def nickname(message):
    if " " in message.text:
        db.updateNickname(message.from_user.id, message.text[message.text.find(" ") + 1:])
        bot.send_message(message.from_user.id, f"Ваш новый никнейм: {message.text[message.text.find(' ') + 1:]}")
    else:
        info = db.profileInfoSQL(message.from_user.id)
        bot.send_message(message.from_user.id, f"Ваш никнейм: {info[1]}\nВведите команду 'Ник [текст]' для смены никнейма")

