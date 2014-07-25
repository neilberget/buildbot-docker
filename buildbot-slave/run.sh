#!/bin/bash

set -e
set -x

docker build -t registry.edmodo.io/buildbot-slave .

docker stop buildbot-slave || true
docker rm buildbot-slave || true

docker run -i -t \
  -e DOCKER_HOST=$DOCKER_HOST \
  --name buildbot-slave \
  --link buildbot-master:bbmaster \
  registry.edmodo.io/buildbot-slave

