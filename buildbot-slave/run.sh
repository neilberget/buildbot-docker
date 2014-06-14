#!/bin/bash

set -e
set -x

docker build -t buildbot-slave .

docker stop buildbot-slave || true
docker rm buildbot-slave || true

docker run -i -t --name buildbot-slave --link buildbot-master:bbmaster buildbot-slave

