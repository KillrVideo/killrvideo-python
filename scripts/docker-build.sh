#!/bin/bash

# Load the version number from environment if provided, otherwise tag as latest
VERSION=${DOCKER_BUILD_TAG:-latest}

docker build -t killrvideo/killrvideo-python:$VERSION .
