import sqlite3
import time
import paho.mqtt.client as mqtt
import database.dbClient
import database.sqliteSetup


topicSensors = "dk/ivy/sensor/#"

def handler(_signal_received, _frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")

    client.disconnect()
    exit(0)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topicSensors)

def on_message(client, userdata, message):
    msg = message.payload.decode('UTF-8')
    print("MQTT: {}", msg)


if __name__ == "__main__":
    database.sqliteSetup.setupDB("dbdata/roomdb.db")
    mqttBroker = "mosquitto"
    client = mqtt.Client("ingest_handler" )
    client.username_pw_set("client", "sekret")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883, 60)
    
    client.loop_forever()

    print("Me ded")