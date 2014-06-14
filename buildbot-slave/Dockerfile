FROM ubuntu:12.04

RUN apt-get update

RUN apt-get install -y python-setuptools
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y git-core

RUN easy_install buildbot-slave

RUN mkdir /buildbot-slave
ADD start_slave.sh /buildbot-slave/start_slave.sh

WORKDIR /buildbot-slave

CMD ["./start_slave.sh"]
