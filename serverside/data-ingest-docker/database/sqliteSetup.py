import sqlite3

def setupDB(name):
    con = sqlite3.connect(name)
    cur = con.cursor()

    cur.execute('''DROP TABLE IF EXISTS occupancy''')
    cur.execute('''DROP TABLE IF EXISTS devices''')
    cur.execute('''DROP TABLE IF EXISTS motion''')
    cur.execute('''DROP TABLE IF EXISTS distance''')

    cur.execute('''CREATE TABLE ocupancy (timestamp Integer, location TEXT, occupied INTEGER)''')
    cur.execute('''CREATE TABLE devices  (timestamp Integer, location TEXT, count Integer)''')
    cur.execute('''CREATE TABLE distance (timestamp Integer, device TEXT, location TEXT, unit TEXT, distance Real)''')
    cur.execute('''CREATE TABLE distance (timestamp Integer, device TEXT, location TEXT, motion Integer)''')

    con.commit()
    con.close()

if __name__ == '__main__':
    setupDB("sensorStorage.db")