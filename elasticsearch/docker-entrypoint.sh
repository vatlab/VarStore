#!/bin/bash

set -e

printf 'discovery.zen.ping.unicast.hosts: ["es:9300"] \n'  >>  /usr/share/elasticsearch/config/elasticsearch.yml
#printf 'discovery.zen.ping.unicast.hosts: ["${DOCKERMACHINE_IP}:9311", "${DOCKERMACHINE_IP}:9312" ]\n'  >>  /usr/share/elasticsearch/config/elasticsearch.yml
printf 'network.host: 0.0.0.0 \n'    >> /usr/share/elasticsearch/config/elasticsearch.yml
printf "discovery.zen.minimum_master_nodes: 1 \n" >> /usr/share/elasticsearch/config/elasticsearch.yml
printf "http.cors.enabled: true \n"               >> /usr/share/elasticsearch/config/elasticsearch.yml
printf "cluster.name: vatlab_cluster \n"        >> /usr/share/elasticsearch/config/elasticsearch.yml
printf 'node.name: vatlab_node \n'             >> /usr/share/elasticsearch/config/elasticsearch.yml
printf 'cluster.routing.allocation.disk.watermark.low : 1gb \n'  >> /usr/share/elasticsearch/config/elasticsearch.yml
printf 'cluster.routing.allocation.disk.watermark.high: 1gb \n'  >> /usr/share/elasticsearch/config/elasticsearch.yml


# Add elasticsearch as command if needed
if [ "${1:0:1}" = '-' ]; then
	set -- elasticsearch "$@"
fi

# Drop root privileges if we are running elasticsearch
# allow the container to be started with `--user`
if [ "$1" = 'elasticsearch' -a "$(id -u)" = '0' ]; then
	# Change the ownership of /usr/share/elasticsearch/data to elasticsearch
	chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data
	
	set -- gosu elasticsearch "$@"
	#exec gosu elasticsearch "$BASH_SOURCE" "$@"
fi

## allow other users to have access to the mounted volume:
chmod -R 777  /usr/share/elasticsearch/data


# As argument is not related to elasticsearch,
# then assume that user wants to run his own process,
# for example a `bash` shell to explore this image
exec "$@"
