# import telebot
import handlers
from config import *

cmds = {
    "help": handlers.help,
    "помощь": handlers.help,
    "команды": handlers.help,
    "профиль": handlers.profileInfo,
    "ник": handlers.nickname,
    "никнейм": handlers.nickname,
    "основные": handlers.helpMain,
    "игровые": handlers.helpGames,
    "развлекательные": handlers.helpFun,
    "клановые": handlers.helpClan
}

@bot.message_handler(content_types=['text'])
def onMessage(message):
    if db.in_db(message.from_user.id):
        if message.text.lower().split()[0] not in cmds:
            handlers.noCom(message)
        for name, func in cmds.items():
            if message.text.lower().split()[0] == name:
                func(message)
                return
    else:
        handlers.reg(message)

bot.polling()
