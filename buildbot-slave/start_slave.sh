#!/bin/bash

set -e
set -x

slave_name=docker-slave
slave_pass=docker-pass

buildslave create-slave slave $BBMASTER_PORT_9989_TCP_ADDR:$BBMASTER_PORT_9989_TCP_PORT $slave_name $slave_pass
buildslave --verbose start --nodaemon slave

