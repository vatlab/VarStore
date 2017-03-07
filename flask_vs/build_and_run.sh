#!/bin/bash


## to build and run only a single elasticsearch container
eval $(docker-machine env default)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip default)


export NAME="flask_vat_vs"

docker stop ${NAME}
docker rm   ${NAME}

docker build -t flask_vs .


docker run -d --name flask_vat_vs -p 80:80 flask_vs