import handlers
from config import *


cmds = {
    "help": handlers.helper,
    "помощь": handlers.helper,
    "команды": handlers.helper,
    "профиль": handlers.profileInfo,
    "ник": handlers.nickname,
    "никнейм": handlers.nickname,
    "основные": handlers.helpMain,
    "игровые": handlers.helpGames,
    "развлекательные": handlers.helpFun,
    "клановые": handlers.helpClan,
    "банк": handlers.bankInfo,
    "баланс": handlers.balance,
    "передать": handlers.give,
    "работа": handlers.jobInfo,
    "работы": handlers.jobList,
    "бонус": handlers.bonus,
    "шар": handlers.magicBall,
    "шанс": handlers.chance
}


@bot.message_handler(content_types=['text'])
def onMessage(message):
    if db.inDb(message.from_user.id):
        if message.text.lower().split()[0] not in cmds:
            handlers.noCom(message)
        for name, func in cmds.items():
            if message.text.lower().split()[0] == name:
                func(message)
                return
    else:
        handlers.reg(message)


bot.polling()
