#!/bin/bash

# Load the version number
#. "`dirname $0`/VERSION"
. "./VERSION"

docker build -t killrvideo/killrvideo-python:$DOCKER_BUILD_TAG .
