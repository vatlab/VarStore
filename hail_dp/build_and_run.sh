#!/bin/bash


## to build and run only a single elasticsearch container
eval $(docker-machine env vat-dp)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip vat-dp)

export NAME="flask_hail_vat_dp"

docker stop ${NAME}
docker rm   ${NAME}

docker build -t hail_flask .


docker run -d --name ${NAME} -v /Users/jma7/Development/hail/test:/usr/work  -v $(pwd)/app:/app  hail_flask python