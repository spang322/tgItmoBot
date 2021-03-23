import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect("players.db",
                                    check_same_thread=False)

        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        players (tg_id INT, name TEXT, money INT)""")
        self.conn.commit()

    def reg(self, name, tg_id):
        self.cur.execute(f"INSERT INTO players VALUES (?, ?, ?)", (tg_id, name, 0))
        self.conn.commit()

    def in_db(self, tg_id):
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