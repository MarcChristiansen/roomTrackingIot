docker run -p 1883:1883 -p 8005:8003 \
	-v /home/$USER/FIND_DATA:/data \
    -e MQTT_ADMIN=ADMIN \
    -e MQTT_PASS=sekret \
    -e MQTT_SERVER='localhost:1883' \
	-e MQTT_EXTERNAL='your public IP' \
	-e MQTT_PORT=1884 \
	--name find3server -d -t schollz/find3