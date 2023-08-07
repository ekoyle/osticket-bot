#!/bin/bash

NETWORK='bhnoc.org'
HOST='osticket_bot'
PROJECT='osticket_bot'
DOCKER_TAG='bhnoc/osticket_bot:latest'
CONTAINER='osticket_bot'
APP_PATH='/Users/nemus/Desktop/git'
mkdir -p $APP_PATH/docker/configs/$CONTAINER
docker stop osticket_bot
docker rm osticket_bot
docker run -d \
	--add-host=osticket_bot.bhnoc.org:127.0.0.1 \
	--cap-add=IPC_LOCK \
	--name osticket_bot \
	--network bhnoc \
	-h osticket_bot \
	--restart unless-stopped \
	-v $APP_PATH/containers/$CONTAINER/config:/opt/env/live/config \
	-v $APP_PATH/containers/$CONTAINER/logs:/opt/env/live/logs \
	-v $APP_PATH/$CONTAINER/app:/opt/env/live/app \
	$DOCKER_TAG
