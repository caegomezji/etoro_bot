#!/bin/bash

docker kill etoro_bot_test
docker rm etoro_bot_test

docker build -t caegomezji/spx500_selenium_test .

docker run -dt \
	--restart always \
	--name=etoro_bot_test \
	--net=host \
	--env-file=.env \
	caegomezji/spx500_selenium_test --port 1888