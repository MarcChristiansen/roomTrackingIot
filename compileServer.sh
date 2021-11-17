docker build -t schollz/find3 serverside/find3-server-docker/
docker build -t webserver/rt  serverside/webserver-docker
docker build -t mqtt/rt 	  serverside/mqtt-server-docker
docker build -t ingest/rt 	  serverside/data-ingest-docker

