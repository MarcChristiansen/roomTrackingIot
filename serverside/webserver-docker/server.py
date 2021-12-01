from flask import Flask
from flask import render_template
from flask import request
from flask_mqtt import Mqtt
from database.dbClient import dbClient
import json
import math

app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = "mosquitto"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_CLIENT_ID"] = "flask_server"
app.config["MQTT_USERNAME"] = "client"
app.config["MQTT_PASSWORD"] = "sekret"

topicLiving = "dk/ivy/occupancy/living"
topicToilet = "dk/ivy/occupancy/toilet"

mqtt = Mqtt(app)

livingOccupied = False
toiletOccupied = False

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    mqtt.subscribe(topicLiving)
    mqtt.subscribe(topicToilet)

@mqtt.on_message()
def handle_message(client, userdata, message):
    dataObject = json.loads(message.payload.decode("UTF-8"))

    if message.topic == topicLiving:
        livingOccupied = dataObject["occupied"]
    
    if message.topic == topicToilet:
        toiletOccupied = dataObject["occupied"]

def getRoomHeat(room):
    dbclient = dbClient("dbdata/roomdb.db") #If error change to "file:dbdata/roomdb.db"
    data = dbclient.get_room_heat(room)

    occupiedData = data.fetchone()
    occupiedCount = occupiedData[1] if occupiedData is not None else 0

    notOccupiedData = data.fetchone()
    notOccupiedCount = notOccupiedData[1] if notOccupiedData is not None else 0

    dbclient.cleanup()

    totalCount = notOccupiedCount + occupiedCount

    if totalCount == 0:
        return 0

    return occupiedCount / totalCount

def getHeatData():
    livingRatio = getRoomHeat("living")
    toiletRatio = getRoomHeat("toilet")

    return livingRatio, toiletRatio

def getOccupancyHistory(room):
    dbclient = dbClient("dbdata/roomdb.db") #If error change to "file:dbdata/roomdb.db"
    data = dbclient.get_room_history(room)

    countArray = [0] * 24
    occupiedArray = [0] * 24

    for row in data:
        timestamp = row[0]
        occupied = row[2]

        dayNorm = timestamp % 86400

        hour = math.floor(dayNorm / 3600)
        
        countArray[hour] += 1

        if occupied:
            occupiedArray[hour] += 1

    dbclient.cleanup()

    histoArray = [0] * 24

    for i in range(24):
        if countArray[i] != 0:
            histoArray[i] = (occupiedArray[i] / countArray[i]) * 100

    return histoArray
            

def createRoomJSONResponse(room):
    occupied = livingOccupied

    if room == "toilet":
        occupied = toiletOccupied

    dataObject = {
        "room": room,
        "occupied": occupied,
        "histogram": getOccupancyHistory(room)
    }

    return json.dumps(dataObject)

def createHeatJSONResponse():
    livingRatio, toiletRatio = getHeatData()
    dataObject = {
        "livingRatio": livingRatio,
        "toiletRatio": toiletRatio
    }

    return json.dumps(dataObject)

def createLiveJSONResponse():
    living = {
        "room": "living",
        "occupied": livingOccupied
    }

    toilet = {
        "room": "toilet",
        "occupied": toiletOccupied
    }

    dataObject = {
        "living": living,
        "toilet": toilet
    }

    return json.dumps(dataObject)

@app.route("/")
def live():
    if request.content_type == "application/json":
        return createLiveJSONResponse()
    return render_template("live.html")

@app.route("/heat")
def heat():
    if request.content_type == "application/json":
        return createHeatJSONResponse()
    return render_template("heat.html")

@app.route("/rooms/living")
def living():
    if request.content_type == "application/json":
        return createRoomJSONResponse("living")
    return render_template("livingRoom.html")

@app.route("/rooms/toilet")
def toilet():
    if request.content_type == "application/json":
        return createRoomJSONResponse("toilet")
    return render_template("toilet.html")

def runServer():
    app.run(debug = True, host="0.0.0.0", port=8010)

if __name__ == "__main__":
    runServer()