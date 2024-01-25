#!/bin/bash

docker kill etoro_bot
docker rm etoro_bot

docker build -t caegomezji/spx500_selenium .

docker run -dt \
	--restart always \
	--name=etoro_bot \
	--net=host \
	--env-file=.env \
	-v ./logs:/usr/app/logs \
	caegomezji/spx500_selenium # -v ./:/usr/app \
