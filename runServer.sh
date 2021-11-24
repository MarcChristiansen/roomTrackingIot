docker run -p 1884:1883 -p 8005:8003 \
	-v /home/$USER/FIND_DATA:/data \
    -e MQTT_ADMIN=client \
    -e MQTT_PASS=sekret \
    -e MQTT_SERVER='localhost:1883' \
	-e MQTT_EXTERNAL='your public IP' \
	-e MQTT_PORT=1884 \
	--name find3serverBaseDocker -d -t schollz/find3
