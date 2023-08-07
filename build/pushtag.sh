#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d")
ENVIRONMENT='latest'
CONTAINER='osticket_bot'

docker tag bhnoc/$CONTAINER:$ENVIRONMENT .dkr.ecr.us-east-1.amazonaws.com/$CONTAINER:$ENVIRONMENT-$TIMESTAMP
docker tag bhnoc/$CONTAINER:$ENVIRONMENT .dkr.ecr.us-east-1.amazonaws.com/$CONTAINER:latest
docker push .dkr.ecr.us-east-1.amazonaws.com/$CONTAINER:$ENVIRONMENT-$TIMESTAMP
docker push .dkr.ecr.us-east-1.amazonaws.com/$CONTAINER:latest
