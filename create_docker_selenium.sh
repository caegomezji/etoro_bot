#!/bin/bash

docker build -t caegomezji/spx500_selenium .

docker run -it --rm \
    --name=etoro_bot \
    --net=host \
    --env-file=.env \
    -v ./:/usr/app \
    caegomezji/spx500_selenium 