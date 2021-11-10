import sqlite3

def setupDB(name):
    con = sqlite3.connect(name)
    cur = con.cursor()

    cur.execute('''DROP TABLE IF EXISTS temperature''')
    cur.execute('''DROP TABLE IF EXISTS humidity''')
    cur.execute('''DROP TABLE IF EXISTS distance''')

    cur.execute('''CREATE TABLE temperature (id TEXT, timestamp Integer, unit TEXT, temperature Integer)''')
    cur.execute('''CREATE TABLE humidity    (id TEXT, timestamp Integer, unit TEXT, humidity Integer)''')
    cur.execute('''CREATE TABLE distance    (id TEXT, timestamp Integer, unit TEXT, distance Real)''')

    con.commit()
    con.close()

if __name__ == '__main__':
    setupDB("sensorStorage.db")