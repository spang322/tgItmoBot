import sqlite3
import datetime
import threading

lock = threading.Lock()


class Database:
    def __init__(self):
        lock.acquire(True)
        self.conn = sqlite3.connect("players.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        lock.release()

    def createDb(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
                players (tg_id INT, name TEXT, money INT, bank INT,
                bank_time DATETIME, bonus DATETIME, coin INT, gold INT,
                bank_extra_time INT, job_num INT, job_time DATETIME,
                work_record INT, job_lvl INT, job_extra_time INT,
                autoShop INT, investAutoShop INT, incomeAutoShop INT, taxAutoShop INT,
                computerShop INT, investComputerShop INT, incomeComputerShop INT, taxComputerShop INT,
                footballClub INT, investFootballClub INT, incomeFootballClub INT, taxFootballClub INT)""")
        self.conn.commit()

    def reg(self, name, tg_id):
        lock.acquire(True)
        self.cur.execute(f"INSERT INTO players VALUES "
                         f"(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (tg_id, name, 5000, 5000,
                          datetime.datetime.today(),
                          datetime.datetime.today(),
                          0, 0, 0, 0,
                          datetime.datetime.now(),
                          0, 1, 0))
        self.conn.commit()
        lock.release()

    def nameExist(self, name):
        lock.acquire(True)
        self.cur.execute(f"SELECT tg_id FROM players WHERE name = ?", (name,))
        if self.cur.fetchone() is None:
            lock.release()
            return True
        else:
            lock.release()
            return False

    def bankMoney(self, tg_id):
        self.cur.execute("SELECT bank_time, bank_extra_time, bank FROM players WHERE tg_id = ?", (tg_id,))
        return self.cur.fetchone()

    def increaseBank(self, tg_id, money, secs, time):
        self.cur.execute(f"UPDATE players SET bank = ? WHERE tg_id = ?", (int(money), tg_id,))
        self.cur.execute(f"UPDATE players SET bank_extra_time = ? WHERE tg_id = ?", (secs, tg_id,))
        self.cur.execute(f"UPDATE players SET bank_time = ? WHERE tg_id = ?", (time, tg_id,))
        self.conn.commit()

    def depositSQL(self, tg_id, money):
        self.cur.execute(f"UPDATE players SET bank = bank+? WHERE tg_id = ?", (money, tg_id,))
        self.cur.execute(f"UPDATE players SET money = money-? WHERE tg_id = ?", (money, tg_id,))
        self.conn.commit()

    def withdrawSQL(self, tg_id, money):
        self.cur.execute(f"UPDATE players SET bank = bank-? WHERE tg_id = ?", (money, tg_id,))
        self.cur.execute(f"UPDATE players SET money = money+? WHERE tg_id = ?", (money, tg_id,))
        self.conn.commit()

    def inDb(self, tg_id):
        self.cur.execute(f"SELECT tg_id FROM players WHERE tg_id = ?", (tg_id,))
        if self.cur.fetchone() is None:
            return False
        else:
            return True

    def nameInDb(self, name):
        self.cur.execute(f"SELECT name FROM players WHERE name = ?", (name,))
        if self.cur.fetchone() is None:
            return False
        else:
            return True

    def profileInfoSQL(self, tg_id):
        self.cur.execute(f"SELECT * FROM players WHERE tg_id = ?", (tg_id,))
        return self.cur.fetchone()

    def updateNickname(self, tg_id, name):
        self.cur.execute(f"UPDATE players SET name = ? WHERE tg_id = ?", (name, tg_id,))
        self.conn.commit()

    def giveSQL(self, receiver, sender, money):
        self.cur.execute(f"UPDATE players SET money = money+? WHERE name = ?", (money, receiver))
        self.cur.execute(f"UPDATE players SET money = money-? WHERE tg_id = ?", (money, sender))
        self.conn.commit()

    def IdByName(self, name):
        self.cur.execute(f"SELECT tg_id FROM players WHERE name = ?", (name,))
        return self.cur.fetchone()

    def jobInfoSQL(self, tg_id):
        self.cur.execute(f"SELECT job_num, job_time, job_lvl, work_record, job_extra_time FROM players WHERE tg_id = ?",
                         (tg_id,))
        return self.cur.fetchone()

    def salary(self, tg_id, money):
        self.cur.execute(f"UPDATE players SET bank = bank+? WHERE tg_id = ?",
                         (money, tg_id,))
        self.cur.execute(f"UPDATE players SET job_time = ? WHERE tg_id = ?",
                         (datetime.datetime.now(), tg_id,))
        self.conn.commit()

    def jobLvlUp(self, tg_id, work_record, extra_seconds):
        self.cur.execute(f"UPDATE players SET work_record = work_record+? WHERE tg_id = ?",
                         (work_record, tg_id,))
        self.cur.execute(f"UPDATE players SET job_extra_time = job_extra_time+? WHERE tg_id = ?",
                         (extra_seconds, tg_id,))
        self.conn.commit()

    def getJobSQL(self, tg_id, job_id):
        self.cur.execute(f"UPDATE players SET job_num = ? WHERE tg_id = ?",
                         (job_id, tg_id))
        self.conn.commit()

    def bonusSQL(self, tg_id):
        self.cur.execute(f"SELECT bonus FROM players WHERE tg_id = ?", (tg_id,))
        return self.cur.fetchone()

    def giveBonus(self, tg_id, money):
        self.cur.execute(f"UPDATE players SET money = money+? WHERE tg_id = ?", (money, tg_id,))
        self.cur.execute(f"UPDATE players SET bonus = ? WHERE tg_id = ?", (datetime.datetime.now(), tg_id,))
        self.conn.commit()

    def businessSQL(self, tg_id):
        self.cur.execute(f"SELECT autoShop INT, investAutoShop INT, incomeAutoShop INT, taxAutoShop INT,"
                         f"computerShop INT, investComputerShop INT, incomeComputerShop INT, taxComputerShop INT,"
                         f"footballClub INT, investFootballClub INT, incomeFootballClub INT, taxFootballClub INT"
                         f" FROM players WHERE tg_id = ?", (tg_id,))
        return self.cur.fetchone()
