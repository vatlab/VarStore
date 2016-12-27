#!/bin/bash

export DOCKERMACHINE_HOST=$(docker-machine ip default)


export ESPORT=9252


## delete index and start over
curl -XDELETE http://${DOCKERIP}:${ESPORT}/gencode

# http DELETE "http://${DOCKERMACHINE_HOST}:${ESPORT}/gencode"


## also delete logs:
rm es.log
rm es_tracer.log
