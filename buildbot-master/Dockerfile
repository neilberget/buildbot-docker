FROM ubuntu:12.04

RUN apt-get update

RUN apt-get install -y python-setuptools
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y git-core

RUN easy_install buildbot

RUN buildbot create-master /buildbot-master
RUN mv /buildbot-master/master.cfg.sample /buildbot-master/master.cfg

EXPOSE 8010
EXPOSE 9989

CMD ["buildbot", "start", "--nodaemon", "/buildbot-master"]
