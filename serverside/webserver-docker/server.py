from flask import Flask
from flask import render_template
from flask import request
from database.dbClient import dbClient

app = Flask(__name__)

def getOccupancyHistory(room):
    dbclient = dbClient("dbdata/roomdb.db") #If error change to "file:dbdata/roomdb.db"
    data = dbclient.get_room_history(room)
    dbclient.cleanup()

#This code is super inefficient and ugly. It could be made more efficient with a database change, but due to time constraints that has not happened
def getHeatData():
    dbclient = dbClient("dbdata/roomdb.db") #If error change to "file:dbdata/roomdb.db"
    data = dbclient.get_occupancy()
    dbclient.cleanup()

    startTime = data[0][0]
    endTime = data[-1][0]
    totalTime = endTime - startTime

    livingTime = 0
    toiletTime = 0

    livingOccupied = False
    toiletOccupied = False

    livingLastTime = 0
    toiletLastTime = 0

    for row in data:
        timestamp = row[0]
        room = row[1]
        occupied = row[2]

        if room == "living":
            if occupied:
                if not livingOccupied:
                    livingOccupied = True
                    livingLastTime = timestamp
            else:
                livingOccupied = False
                livingTime += (timestamp - livingLastTime)

        if room == "toilet":
            if occupied:
                if not toiletOccupied:
                    toiletOccupied = True
                    toiletLastTime = timestamp
            else:
                toiletOccupied = False
                toiletTime += (timestamp - toiletLastTime)
    
    livingRatio = livingTime / totalTime
    toiletRatio = toiletTime / totalTime

    return livingRatio, toiletRatio

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
    app.jinja_env.globals.update(getHeatData=getHeatData)
    app.run(debug = True, host="0.0.0.0", port=80)

if __name__ == "__main__":
    runServer()