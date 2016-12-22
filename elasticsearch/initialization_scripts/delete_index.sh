#!/bin/bash

export DOCKERMACHINE_HOST=$(docker-machine ip lms)


export ESPORT=9251


## delete index and start over
#curl -X DELETE http://${DOCKERIP}:${ESPORT}/lung/

http DELETE "http://${DOCKERMACHINE_HOST}:${ESPORT}/vatvs"


## also delete logs:
rm es.log
rm es_tracer.log
