# from telebot import types
from config import *

def help(message):
    if " " in message.text:
        second_word = message.text.split()[1]
        if second_word.lower() == "основные" or second_word.lower() == "1":
            helpMain(message)
        elif second_word.lower() == "игровые" or second_word.lower() == "2":
            helpGames(message)
        elif second_word.lower() == "развлекательные" or second_word.lower() == "3":
            helpFun(message)
        elif second_word.lower() == "клановые" or second_word.lower() == "4":
            helpClan(message)
        else:
            bot.send_message(message.from_user.id, "Такой команды нет")
    else:
        bot.send_message(message.from_user.id, """Вот список команд:
    1. Основные
    2. Игровые
    3. Развлекательные
    4. Клановые
    
    Репорт [текст] - есть вопросы? Задавай!
    Беседы - места, где можно поиграть в бота""")

def helpMain(message):
    bot.send_message(message.from_user.id, """Основные команды:
    Профиль - сделано
    Ник [текст] - сделано
    Баланс
    Банк
        Банк положить [сумма]
        Банк снять [сумма]
    Передать [никнейм][сумма][комментарий]
    Работа
    Бизнес
    Топ
        Топ кланов
        Топ богатых
        Топ мафии
    Магазин
    Бонус
    Настройки""")

def helpGames(message):
    bot.send_message(message.from_user.id, """Игровые команды:
    Мафия
    Перестрелка
    Ставка
    Лотерея
    Казино
        Казино коины
        Поставить [сумма]
        Казино стоп""")

def helpFun(message):
    bot.send_message(message.from_user.id, """Развлекательные команды:
    Вики [текст]
    Шар [текст]
    Шанс
    Кто/кому/кого
    Свадьба [никнейм]
        Брак развод
    Погода [город]
    Дата""")

def helpClan(message):
    bot.send_message(message.from_user.id, """Клановые команды:
    Клан
    Клан создать [название]
    Клан переименовать [название]
    Клан участники
        Клан участник [никнейм]
    Клан пригласить [никнейм]
        Клан приглашения
    Клан повысить [никнейм]
    Клан понизить [никнейм]
    Клан зарплата [сумма]
        Клан пополнить [сумма]
    Клан бизнес
    Клан возможности
    Клан выгнать [никнейм]
    Клан покинуть""")

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
    bot.send_message(message.from_user.id, f"ID: {info[0]}\nНик: {info[1]}\nДенег: {info[2]}$")

def nickname(message):
    if " " in message.text:
        db.updateNickname(message.from_user.id, message.text[message.text.find(" ") + 1:])
        bot.send_message(message.from_user.id, f"Ваш новый никнейм: {message.text[message.text.find(' ') + 1:]}")
    else:
        info = db.profileInfoSQL(message.from_user.id)
        bot.send_message(message.from_user.id, f"Ваш никнейм: {info[1]}\nВведите команду 'Ник [текст]' для смены никнейма")

