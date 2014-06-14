#!/bin/bash

set -e
set -x

buildslave create-slave slave $BBMASTER_PORT_9989_TCP_ADDR:$BBMASTER_PORT_9989_TCP_PORT example-slave pass
buildslave start --nodaemon slave

