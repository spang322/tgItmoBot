from math import floor
from config import *
from random import randint, choice
import datetime


def helper(message):
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
    Баланс - сделано
    Банк - сделано
        Банк положить [сумма] - сделано
        Банк снять [сумма] - сделано
    Передать [никнейм] [сумма] - сделано
    Работа - сделано
    Бизнес
    Топ
        Топ кланов
        Топ богатых
        Топ мафии
    Магазин
    Бонус - сделано (FIXME)
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
    Шар [текст] - сделано
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
    if db.nameExist(message.text):
        db.reg(message.text, message.from_user.id)
        info = db.profileInfoSQL(message.from_user.id)
        bot.send_message(message.from_user.id, f"Информация о профиле:\n"
                                               f"ID: {info[0]}\n"
                                               f"Ник: {info[1]}\n"
                                               f"Денег: {info[2]}$\n"
                                               f"В банке: {info[3]}$")
    else:
        bot.send_message(message.from_user.id, "Такой ник уже занят\nВведите другой")
        bot.register_next_step_handler(message, createProfile)


def profileInfo(message):
    info = db.profileInfoSQL(message.from_user.id)
    bot.send_message(message.from_user.id, f"Информация о профиле:\n"
                                           f"ID: {info[0]}\n"
                                           f"Ник: {info[1]}\n"
                                           f"Денег: {info[2]}$\n"
                                           f"В банке: {info[3]}$")


def nickname(message):
    if " " in message.text:
        db.updateNickname(message.from_user.id, message.text[message.text.find(" ") + 1:])
        bot.send_message(message.from_user.id, f"Ваш новый никнейм: {message.text[message.text.find(' ') + 1:]}")
    else:
        info = db.profileInfoSQL(message.from_user.id)
        bot.send_message(message.from_user.id, f"Ваш никнейм: {info[1]}\n"
                                               f"Введите команду 'Ник [текст]' для смены никнейма")


def balance(message):
    info = db.profileInfoSQL(message.from_user.id)
    bot.send_message(message.from_user.id, f"Информация о баланса:\n"
                                           f"Денег: {info[2]}$\n"
                                           f"В банке: {info[3]}$\n"
                                           f"Blincoin: {info[6]}\n"
                                           f"Blingold: {info[7]}")


def bankInfo(message):
    if " положить" in message.text:
        try:
            money = int(message.text[message.text.rfind(" ") + 1:])
            deposit(message, money)
        except ValueError:
            bot.send_message(message.from_user.id, "Неверно указана сумма")
    elif " снять" in message.text:
        try:
            money = int(message.text[message.text.rfind(" ") + 1:])
            withdraw(message, money)
        except ValueError:
            bot.send_message(message.from_user.id, "Неверно указана сумма")
    else:
        bankPercent(message)
        bank = db.bankMoney(message.from_user.id)
        bot.send_message(message.from_user.id, f"На вашем счету: {bank[2]}$\n"
                                               f"В час капает: {int(bank[2] * 0.05)}$")


def bankPercent(message):
    bank = db.bankMoney(message.from_user.id)
    time1 = datetime.datetime.fromisoformat(bank[0])
    time2 = datetime.datetime.now()
    diff = time2 - time1
    diff = diff.seconds + bank[1]
    money = bank[2] * (1.05 ** (diff // 3600))
    db.increaseBank(message.from_user.id, money, diff % 15, datetime.datetime.now())


def deposit(message, money):
    info = db.profileInfoSQL(message.from_user.id)
    if info[2] >= money:
        bankPercent(message)
        db.depositSQL(message.from_user.id, money)
        bot.send_message(message.from_user.id, f"Вы положили на счет {money}$")
    else:
        bot.send_message(message.from_user.id, "Недостаточно средств")


def withdraw(message, money):
    info = db.profileInfoSQL(message.from_user.id)
    if info[3] >= money:
        bankPercent(message)
        db.withdrawSQL(message.from_user.id, money)
        bot.send_message(message.from_user.id, f"Вы сняли со счета {money}$")
    else:
        bot.send_message(message.from_user.id, "Недостаточно средств")


def give(message):
    try:
        money = int(message.text[message.text.rfind(" ") + 1:])
        nick = message.text[message.text.find(" ") + 1:message.text.rfind(" ")]
        info = db.profileInfoSQL(message.from_user.id)
        if info[2] >= money:
            if money > 0:
                if db.nameInDb(nick):
                    db.giveSQL(nick, message.from_user.id, money)
                    bot.send_message(message.from_user.id, f"Вы успешно перевели {money}$ игроку {nick}")
                    bot.send_message(db.IdByName(nick)[0], f"Игрок {info[1]} перевел вам {money}$")
                else:
                    bot.send_message(message.from_user.id, "Игрока с таким ником не существует")
            else:
                bot.send_message(message.from_user.id, "Неверно введена сумма")
        else:
            bot.send_message(message.from_user.id, "Недостаточно средств")
    except ValueError:
        bot.send_message(message.from_user.id, "Неверно введена сумма")


def jobRefresh(message):
    info = db.jobInfoSQL(message.from_user.id)
    time1 = datetime.datetime.fromisoformat(info[1])
    time2 = datetime.datetime.now()
    diff = time2 - time1
    extra_seconds = diff.seconds - floor(diff.seconds / 3600)
    diff = floor(diff.seconds / 3600)
    db.jobLvlUp(message.from_user.id, diff, extra_seconds)
    return diff


def jobInfo(message):
    job_refresh = jobRefresh(message)
    diff = job_refresh
    info = db.jobInfoSQL(message.from_user.id)
    money = 1000 * (2 ** info[0]) * diff
    if " " in message.text:
        try:
            job_num = int(message.text.split()[1])
            if job_num == 0:
                bot.send_message(message.from_user.id, f"Вы не можете устроиться безработным")
            elif job_num == info[0]:
                bot.send_message(message.from_user.id, f"Вы уже работаете {jobs[job_num]}")
            elif job_num <= info[2]:
                db.getJobSQL(message.from_user.id, job_num)
                bot.send_message(message.from_user.id, f"Поздравляю, вы устроились {jobs[job_num]}")
            else:
                bot.send_message(message.from_user.id, "Вы недостаточно квалифицированы для этой работы")
        except ValueError:
            bot.send_message(message.from_user.id, "Неверно указан номер работы")
    else:
        if info[0] == 0:
            bot.send_message(message.from_user.id, "Вы безработный\n"
                                                   "Посмотрите список доступных вам работ с помощью команды 'Работы'")
        else:
            if money == 0:
                bot.send_message(message.from_user.id, f"Вы работаете {jobs[info[0]]}\n"
                                                       f"Вы совсем недавно получали зарплату, поработайте еще немного!\n"
                                                       f"Вы можете посмотреть список доступных вам работ с помощью команды 'Работы'")
            else:
                bot.send_message(message.from_user.id, f"Вы работаете {jobs[info[0]]}\n"
                                                       f"Вы работали {diff} часов и получили зарплату в размере {money}$\n"
                                                       f"Вы можете посмотреть список доступных вам работ с помощью команды 'Работы'")
                db.salary(message.from_user.id, money)


def jobList(message):
    jobRefresh(message)
    info = db.jobInfoSQL(message.from_user.id)
    job_list = ''
    for i in range(1, info[2] + 1):
        job_list += jobs[i].capitalize() + "\n"
    bot.send_message(message.from_user.id, f"Вы можете работать\n"
                                           f"{job_list}"
                                           f"Ваш уровень: {info[2]}\n"
                                           f"Чем выше уровень, тем больше работ вам будут доступны\n"
                                           f"Вы можете сменить работу с помощью команды 'Работа [номер]'")


def bonus(message):
    info = db.bonusSQL(message.from_user.id)
    time = datetime.datetime.fromisoformat(info[0])
    print(time)
    # time_left = datetime.time(time.hour, time.minute, time.second) - FIXME
    day = datetime.datetime.now()
    print(day)
    # time_now = datetime.time(day.hour, day.minute, day.second) - FIXME
    diff1 = day - time
    print(type(diff1.min))
    # diff2 = datetime.timedelta() - FIXME
    if diff1.days >= 1:
        money = randint(5000, 50000)
        db.giveBonus(message.from_user.id, money)
        bot.send_message(message.from_user.id, f"Вам выдан бонус в размере {money}")
    else:
        bot.send_message(message.from_user.id, f"Вы уже получали бонус сегодня\n")
        # f"Следующий бонус можно получить через {diff2}")


def magicBall(message):
    bot.send_message(message.from_user.id, choice(magic_ball))


def chance(message):
    bot.send_message(message.from_user.id, choice(chance_phrases) + str(randint(0, 100)) + "%")


def business(message):
    pass
