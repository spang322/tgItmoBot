# import telebot
import handlers
from config import *

cmds = {
    "help": handlers.help,
    "помощь": handlers.help
}

@bot.message_handler(content_types=['text'])
def onMessage(message):
    if db.in_db(message.from_user.id):
        if message.text.lower() not in cmds:
            handlers.noCom(message)
        for name, func in cmds.items():
            if message.text.lower() == name:
                func(message)
                return
    else:
        handlers.reg(message)

bot.polling()
