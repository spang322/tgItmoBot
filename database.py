import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect("players.db",
                                    check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        players (id INT, name TEXT, money INT)""")
        self.conn.commit()