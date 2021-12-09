# Introduction
This system is designed to monitor occupancy using a variety of sensors including motion, distance and Find3

# Setup overview
Setup requires quite a few things in terms of hardware. If an example is required it is recommended to look at the demonstration on: http://iot.marcs.dk:8010

Requirements
RPI 3/4 patched with nexmon, docker, and find3 scanners.
RPI W patched with nexmon, docker, and find3 scanners.

Nexmon: https://github.com/seemoo-lab/nexmon
Find3 scanner: https://www.internalpositioning.com/doc/cli-scanner.md

## Running sensors on RPI 3/4
use the following to compile:
```
./compileSensors.sh
```
And modify runSensorsTemplate.sh. Save it as runSensors.sh and use:
```
./runSensors.sh
```
The motion sensor (HCSR501) is connected on port 25 and the distance sensor (HCSR05) is connected on port 23 (TRIGGER) and port 24 (ECHO)

Edit the ip on line 46 in sensors/sensorPublish.py to match the ip of the server it has to connect to.

## Running server.
```
./runServer.sh
docker-compose -f docker-composeCloud.yml up
```

Also ensure that the IP in line 114 in severside/data-ingest-docker/data_ingest.py is the local IP of the server it is running on. The reason this is required is that docker-compose did not work properly with the find3 server. This causes the find3 MQTT to not recieve any updates which renders it useless. The only solution was to host it via normal docker and thus this workaround was required.
