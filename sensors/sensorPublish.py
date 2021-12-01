from logging import error
from motionSensor.HCSR501 import hcsr501Sensor
from distanceSensor.HCSR05 import hcsr05Sensor
import time
import paho.mqtt.client as mqtt
import uuid
import os
from signal import signal, SIGINT
from sys import exit
import json
import paho.mqtt.client as mqtt


hcsr501 = hcsr501Sensor(25)
hcsr05 = hcsr05Sensor(23, 24)

rpId = os.environ['RPI_ID']
room = os.environ['ROOM_NAME']

def connect_broker(connectionString, clientName):
    client = mqtt.Client(clientName)
    client.username_pw_set("client", "sekret")
    client.connect(connectionString, 1883, 60)
    return client

topicMotionCloud    = "dk/ivy/sensor/"+ rpId +"/motion"
topicDistanceCloud    = "dk/ivy/sensor/"+ rpId +"/distance"

messageMotion   = {"unit": "bool", "id": rpId, "room": room}
messageDistance = {"unit": "cm", "id": rpId, "room": room}


def handler(_signal_received, _frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    hcsr501.cleanup()
    hcsr05.cleanup()
    cloudClient.disconnect()
    cloudClient.loop_stop()
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, handler)

    cloudClient = connect_broker("teamspeak.marcs.dk", "motion_and_distance_sensor_" + rpId) #Cloud

    cloudClient.loop_start()
    
    while True:
        motion = hcsr501.get_motion()
        distance = hcsr05.get_distance()

        messageDistance["timestamp"] = messageMotion["timestamp"] = int(time.time())

        messageMotion["value"] = motion
        messageDistance["value"] = distance

        cloudClient.publish(topicMotionCloud, json.dumps(messageMotion))
        cloudClient.publish(topicDistanceCloud, json.dumps(messageDistance))

        print("Motion detected:", motion)
        print("Distance:", distance)
        time.sleep(2)

