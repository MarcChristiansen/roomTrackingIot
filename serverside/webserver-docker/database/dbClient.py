import sqlite3

class dbClient(object):
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    def get_room_history(self, room):
        return self.cur.execute("SELECT * FROM occupancy WHERE location='" + room + "'")    

    def get_room_heat(self, room):
        return self.cur.execute("SELECT occupied, COUNT(*) AS count FROM occupancy WHERE location='" + room + "' GROUP BY occupied ORDER BY occupied DESC")

    def cleanup(self):
        self.con.close()