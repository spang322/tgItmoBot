import telebot
import handlers
import database

cmds = {
    "help": handlers.help,
    "помощь": handlers.help
}

bot = telebot.TeleBot("1775120188:AAGjSTkWgUwxwkJfQjEU74dPBvic9FAqkNw")

@bot.message_handler(content_types=['text'])
def onMessage(message):
    for name, func in cmds.items():
        if message.text.lower() == name:
            func(bot, message)
            return

bot.polling()