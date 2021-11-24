import sqlite3

class dbClient(object):
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    def get_room_history(self, room):
        return self.cur.execute("SELECT * FROM occupancy WHERE location=" + room)    

    def cleanup(self):
        self.con.close()