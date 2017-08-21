#!/bin/bash


## to build and run only a single elasticsearch container
eval $(docker-machine env vat-dp)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip vat-dp)

export DOCKERNAME="vat_flask_hail_dp"
export IMAGENAME="flask_hail_dp"

docker stop ${DOCKERNAME}
docker rm   ${DOCKERNAME}

docker build -t ${IMAGENAME} .


docker run -d --name ${DOCKERNAME} -p 80:80 -v $(pwd)/app:/app -v /Users/jma7/Development/hail/test:/usr/work  ${IMAGENAME}  python /app/main.py