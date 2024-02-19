#!/bin/bash

docker kill etoro_bot_test
docker rm etoro_bot_test

docker build -t caegomezji/spx500_selenium_test .
docker run -it \
	--restart always \
	--name=etoro_bot_test \
	--net=host \
	--env-file=.env.test \
	-v ./:/usr/app \
	caegomezji/spx500_selenium_test --reload --port 1888