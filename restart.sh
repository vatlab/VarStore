#!/bin/bash


eval $(docker-machine env default)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip default)

containers=("elasticsearch_dp")

echo "Stopping and removing old containers"
for c in "${containers[@]}"; do
	docker stop ${c}
	docker rm   ${c}
done

docker-compose -f docker-compose-development-up.yml  build 
echo "Finished build; starting up"

docker-compose -f docker-compose-development-up.yml up -d
echo "Finished"
