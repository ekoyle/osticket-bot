#!/bin/bash

NETWORK='bhnoc.org'
HOST='osticket_bot'
PROJECT='osticket_bot'
DOCKER_TAG='bhnoc/osticket_bot:latest'
CONTAINER='osticket_bot'
LOG_PATH='/home/bhnoc/logs'
mkdir -p $LOG_PATH/$CONTAINER/
APP_PATH='/home/bhnoc/git/base/docker/'
docker stop osticket_bot
docker rm osticket_bot
docker run -d \
	--add-host=osticket_bot.fuzeflow.com:127.0.0.1 \
	-p8200:8200 \
	--cap-add=IPC_LOCK \
	--name osticket_bot \
	--network bhnoc \
	-h osticket_bot \
	--restart unless-stopped \
	-v $APP_PATH/logs/osticket_bot:/var/log/osticket_bot/ \
	-v $APP_PATH/configs/$CONTAINER/config:/opt/env/live/config \
	-v $APP_PATH/configs/$CONTAINER/logs:/opt/env/live/logs \
	-v $APP_PATH/$CONTAINER/app:/opt/env/live/app \
	$DOCKER_TAG
