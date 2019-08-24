#!/bin/bash

# command to run supporting KillrVideo infrastructure via docker-compose and
# Python services directly on the host machine (outside docker)

# NOTE: run this from the root killrvideo-python directory
#   scripts/run-docker-backend-external.sh

# setting environment variable to the IP address of the host
export KILLRVIDEO_BACKEND=`ipconfig getifaddr en0`

# the compose file swaps in the value of `KILLRVIDEO_BACKEND` in several places
docker-compose -p killrvideo-python -f docker-compose-backend-external.yaml up -d
 
