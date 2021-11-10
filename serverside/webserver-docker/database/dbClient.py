import sqlite3

class dbClient(object):
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    def get_data(self, table):
        return self.cur.execute("SELECT * FROM " + table)
    
    def add_entry(self, id, sensor, timestamp, unit, value):
        self.cur.execute("INSERT INTO {} VALUES ('{}' , {} , '{}' , {})".format(id, sensor, int(timestamp), unit, value))
        self.con.commit()

    def get_unique_ids(self):
        return self.cur.execute("SELECT DISTINCT id FROM temperature")        

    def cleanup(self):
        self.con.close()