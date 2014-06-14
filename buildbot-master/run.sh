#!/bin/bash

set -e
set -x

docker build -t buildbot .
docker stop buildbot-master || true
docker rm buildbot-master || true
docker run -i -t -p 8010:8010 -p 9989:9989 --name buildbot-master buildbot
