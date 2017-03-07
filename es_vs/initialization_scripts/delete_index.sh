#!/bin/bash

export DOCKERMACHINE_HOST=$(docker-machine ip default)


export ESPORT=9251


## delete index and start over
#curl -X DELETE http://${DOCKERIP}:${ESPORT}/lung/

curl -XDELETE "http://${DOCKERMACHINE_HOST}:${ESPORT}/vatdpalt"


## also delete logs:
rm es.log
rm es_tracer.log
