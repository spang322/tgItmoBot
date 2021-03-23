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

    def profileInfo(self, tg_id):
        self.cur.execute(f"SELECT * FROM players WHERE tg_id = ?", (tg_id,))
        return self.cur.fetchone()