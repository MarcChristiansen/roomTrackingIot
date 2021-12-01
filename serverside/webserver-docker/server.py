from flask import Flask
from flask import render_template
from flask import request
from database.dbClient import dbClient

app = Flask(__name__)

def getOccupancyHistory(room):
    dbclient = dbClient("dbdata/roomdb.db") #If error change to "file:dbdata/roomdb.db"
    data = dbclient.get_room_history(room)
    dbclient.cleanup()

@app.route("/")
def index():
    return render_template("live.html")

@app.route("/heat")
def live():
    return render_template("heat.html")

@app.route("/rooms/living")
def living():
    return render_template("livingRoom.html")

@app.route("/rooms/toilet")
def toilet():
    return render_template("toilet.html")

def runServer():
    app.run(debug = True, host="0.0.0.0", port=80)

if __name__ == "__main__":
    runServer()