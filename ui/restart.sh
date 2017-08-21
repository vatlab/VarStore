#!/bin/bash


# eval $(docker-machine env default)

# export DOCKERMACHINE_HOSTNAME=$(docker-machine ip default)

# containers=("es-vat-vs-1"  "es-vat-vs-2" "flask_vat_vs")

# echo "Stopping and removing old containers"
# for c in "${containers[@]}"; do
# 	docker stop ${c}
# 	docker rm   ${c}
# done

# docker-compose -f docker-compose-up-vat-vs.yml  build 
# echo "Finished build; starting up"

# docker-compose -f docker-compose-up-vat-vs.yml up -d
# echo "Finished"


eval $(docker-machine env vat-dp)

export DOCKERMACHINE_HOSTNAME=$(docker-machine ip vat-dp)

containers=("es-vat-dp-1"  "es-vat-dp-2" "flask_vat_dp")

echo "Stopping and removing old containers"
for c in "${containers[@]}"; do
	docker stop ${c}
	docker rm   ${c}
done

docker-compose -f docker-compose-up-vat-dp.yml  build 
echo "Finished build dp; starting up"

docker-compose -f docker-compose-up-vat-dp.yml up -d
echo "Finished dp"