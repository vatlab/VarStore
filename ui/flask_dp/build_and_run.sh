#!/bin/bash


## to build and run only a single elasticsearch container
eval $(docker-machine env vat-dp)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip vat-dp)

export NAME="flask_vat_dp"

docker stop ${NAME}
docker rm   ${NAME}

docker build -t flask_dp .


docker run -d --name flask_vat_dp -p 80:80 -v $(pwd)/app:/app flask_dp python /app/main.py