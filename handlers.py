from telebot import types

def help(bot, message):
    bot.send_message(message.from_user.id, "Бог поможет")