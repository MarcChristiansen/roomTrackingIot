import sqlite3

class dbClient(object):
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    def get_data(self, table):
        return self.cur.execute("SELECT * FROM " + table)
    
    def add_distance(self,timestamp, device, location, unit, value):
        self.cur.execute("INSERT INTO distance VALUES ('{}' , {} , '{}' , {})".format(int(timestamp), device, location, unit, value))
        self.con.commit()

    def add_motion(self, timestamp, device, location, motion):
        self.cur.execute("INSERT INTO motion VALUES ('{}' , {} , '{}' , {})".format(int(timestamp), device, location, motion))
        self.con.commit()

    def add_device_count(self, timestamp, location, amount):
        self.cur.execute("INSERT INTO devices VALUES ('{}' , {} , '{}' , {})".format(int(timestamp), location, amount))
        self.con.commit()

    def add_ocupancy(self, timestamp, location, occupied):
        self.cur.execute("INSERT INTO ocupancy VALUES ('{}' , {} , '{}' , {})".format(int(timestamp), location, occupied))
        self.con.commit()

    def cleanup(self):
        self.con.close()