#!/bin/bash


## to build and run only a single elasticsearch container

export imageNAME="elasticsearch_dp"
export dockerNAME="elasticsearch_dp"

docker stop ${dockerNAME}
docker rm   ${dockerNAME}

docker build -t ${imageNAME} .

export HERE=`pwd`

mkdir -p ${HERE}/elasticsearch_data

docker run -d -p 9225:9200 -p 9325:9300 \
     -v ${HERE}/elasticsearch_data:/usr/share/elasticsearch/data \
     -v ${HERE}/scripts:/root/scripts \
     --name ${dockerNAME} ${imageNAME}
