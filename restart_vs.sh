#!/bin/bash


eval $(docker-machine env default)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip default)

containers=("es-vat-vs-1"  "es-vat-vs-2")

echo "Stopping and removing old containers"
for c in "${containers[@]}"; do
	docker stop ${c}
	docker rm   ${c}
done

docker-compose -f docker-compose-up-vat-vs.yml  build 
echo "Finished build vs ; starting up"

docker-compose -f docker-compose-up-vat-vs.yml up -d
echo "Finished vs"


