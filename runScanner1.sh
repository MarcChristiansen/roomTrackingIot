docker run --net="host" --privileged --name scanner -d -i -t schollz/find3-cli-scanner

docker exec scanner sh -c "find3-cli-scanner -i wlan0 -device DEVICE -family family -wifi -bluetooth -forever -server 192.168.1.161:8005 -scantime 10 -bluetooth -forever -passive &"

docker start scanning