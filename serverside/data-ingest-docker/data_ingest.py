import sqlite3
import time
import paho.mqtt.client as mqtt
from database.dbClient import dbClient
from database.sqliteSetup import setupDB
import os
import threading
import json
import functools
from signal import signal, SIGINT


topicSensors = "dk/ivy/sensor/#"
topicSensorsPrefix = topicSensors[:-1]
baseTopicOccupancy = "dk/ivy/occupancy/"

#Find3 related variables
topicFind3 = "test/location/#"

find3DeviceSet = {"wifi-98:09:cf:8c:1d:52"}


#Timeouts for sensors in seconds. Controls how long a room will be occupied from a given sensor firing
motionSensorTimeout = 30 
find3Timeout = 90

def handler(_signal_received, _frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")

    client.loop_stop(force=False)
    client.disconnect()
    find3_client.loop_stop(force=False)
    find3_client.disconnect()
    exit(0)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topicSensors)

def on_connect_find3(client, userdata, flags, rc):
    client.subscribe(topicFind3)

def occupyRoomWithTimeout(currentOccupancy, occupancyTimeout, dictLock, dbclient, client, room, timeout):
    if(currentOccupancy.get(room) == None or currentOccupancy[room] == False):
        dbclient.add_ocupancy(time.time(), room, 1)
    with dictLock:
        currentOccupancy[room] = True
        occupancyTimeout[room] = time.time() + timeout
        
    print(room + f" is now occupied for {timeout} seconds") #TODO remove'

    ndict = {"room": room, "occupied":True}
    client.publish(baseTopicOccupancy+room, json.dumps(ndict), retain=True)

def on_message(currentOccupancy, occupancyTimeout, dictLock, dbclient, client, userdata, message):
    msgStr = message.payload.decode('UTF-8')
    #print(message.topic)
    #print(msgStr)
    #print(topicSensorsPrefix)
    if(message.topic.startswith(topicSensorsPrefix)):
        dataObject = json.loads(message.payload.decode("UTF-8"))

        if(message.topic.endswith("motion") and bool(dataObject["value"])):
            dbc.add_motion(dataObject["timestamp"], dataObject["id"], dataObject["room"], int(dataObject["value"] == True))
            occupyRoomWithTimeout(currentOccupancy, occupancyTimeout, dictLock, dbclient, client, dataObject["room"], motionSensorTimeout)

        if(message.topic.endswith("distance")):
            dbc.add_distance(dataObject["timestamp"], dataObject["id"], dataObject["room"], dataObject["unit"], dataObject["value"])
            pass # TODO handle distance
    #print("MQTT: {}", msg)

def on_message_find3(currentOccupancy, occupancyTimeout, dictLock, find3DeviceSet, dbclient, standard_client, find3_client, userdata, message):
    msgStr = message.payload.decode('UTF-8')
    if(message.topic.rsplit('/', 1)[-1] in find3DeviceSet):
        print(message.topic)
        dataObject = json.loads(message.payload.decode("UTF-8"))
        room = dataObject["location"]
        print(f"Device {message.topic} is in {room}")
        occupyRoomWithTimeout(currentOccupancy, occupancyTimeout, dictLock, dbclient, standard_client, room, find3Timeout)


def occupancyTimeoutCheck(currentOccupancy, occupancyTimeout, dictLock, client, dbclient):
    while True: #Do forever
        time.sleep(5) #Delay for when to check if occupancy timeout is over.
        print("Timeout check: Current occupancy", currentOccupancy)
        with dictLock:
            for room, occupied in currentOccupancy.items():
                if occupied and occupancyTimeout[room] < time.time():
                    currentOccupancy[room] = False
                    dbclient.add_ocupancy(time.time(), room, 0)
                    ndict = {"room": room, "occupied":False}
                    client.publish((baseTopicOccupancy + room), json.dumps(ndict), retain=True)
                    print("Room {} is now empty as timeout ran out...")
            


if __name__ == "__main__":
    signal(SIGINT, handler)

    setupDB("file:dbdata/roomdb.db")
    dbc = dbClient("file:dbdata/roomdb.db")

    dictLock = threading.Lock() #Use lock before modifying or reading dicts... TODO ensure performance is reasonable
    currentOccupancy = {}
    occupancyTimeout = {}

    mqttBroker = "mosquitto"
    client = mqtt.Client("ingest_handler" )
    client.username_pw_set("client", "sekret")
    client.on_connect = on_connect
    client.on_message = functools.partial(on_message, currentOccupancy, occupancyTimeout, dictLock, dbc)
    client.connect(mqttBroker, 1883, 60)
    
    client.loop_start()

    mqttBroker_find3 = "192.168.1.161"
    find3_client = mqtt.Client("ingest_handler_find3" )
    find3_client.username_pw_set("client", "sekret")
    find3_client.on_connect = on_connect_find3
    find3_client.on_message = functools.partial(on_message_find3, currentOccupancy, occupancyTimeout, dictLock, find3DeviceSet, dbc, client)
    find3_client.connect(mqttBroker_find3, 1884, 60)

    find3_client.loop_start()

    print("Hej")

    occupancyTimeoutCheck(currentOccupancy, occupancyTimeout, dictLock, client, dbc)