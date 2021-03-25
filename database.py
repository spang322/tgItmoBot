import sqlite3
import datetime

class database:
    def __init__(self):
        self.conn = sqlite3.connect("players.db",
                                    check_same_thread=False)

        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        players (tg_id INT, name TEXT, money INT, bank INT,
        bank_time DATETIME, bonus DATE, coin INT, gold INT,
        bank_extra_time INT)""")
        self.conn.commit()

    def reg(self, name, tg_id):
        self.cur.execute(f"INSERT INTO players VALUES "
                         f"(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (tg_id, name, 5000, 5000,
                          datetime.datetime.today(),
                          datetime.date.today(),
                          0, 0, 0))
        self.conn.commit()

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
        if self.cur.fetchone() == None:
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
