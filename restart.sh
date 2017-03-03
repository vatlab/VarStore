#!/bin/bash


eval $(docker-machine env default)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip default)

containers=("es-vat-vs-1"  "es-vat-vs-2"  "es-vat-dp-1"  "es-vat-dp-2")

echo "Stopping and removing old containers"
for c in "${containers[@]}"; do
	docker stop ${c}
	docker rm   ${c}
done

docker-compose -f docker-compose-up.yml  build 
echo "Finished build; starting up"

docker-compose -f docker-compose-up.yml up -d
echo "Finished"
