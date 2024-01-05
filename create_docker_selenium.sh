#!/bin/bash

docker build -t caegomezji/spx500_selenium .

docker run -dt \
    --restart always \
    --name=etoro_bot \
    --net=host \
    --env-file=.env \
    -v ./:/usr/app \
    caegomezji/spx500_selenium 