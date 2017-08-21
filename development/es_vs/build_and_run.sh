#!/bin/bash


## to build and run only a single elasticsearch container

export NAME="elasticsearch_cl"

docker stop ${NAME}
docker rm   ${NAME}

docker build -t ${NAME} .

export HERE=`pwd`

mkdir -p ${HERE}/elasticsearch_data

docker run -d -e "TERM=xterm" -p 9200:9200 -p 9300:9300 \
     -v ${HERE}/elasticsearch_data:/usr/share/elasticsearch/data \
     -v ${HERE}/scripts:/root/scripts \
     --name ${NAME} ${NAME}
