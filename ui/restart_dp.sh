#!/bin/bash


eval $(docker-machine env vat-dp)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip vat-dp)

containers=("es-vat-dp-1"  "es-vat-dp-2")

echo "Stopping and removing old containers"
for c in "${containers[@]}"; do
	docker stop ${c}
	docker rm   ${c}
done

docker-compose -f docker-compose-up-vat-dp.yml  build 
echo "Finished build dp; starting up"

docker-compose -f docker-compose-up-vat-dp.yml up -d
echo "Finished dp"