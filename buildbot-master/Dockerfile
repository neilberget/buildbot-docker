FROM ubuntu:12.04

RUN apt-get update

RUN apt-get install -y python-setuptools
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y git-core
RUN apt-get install -y python-pip

RUN easy_install buildbot

RUN buildbot create-master /buildbot-master

RUN apt-get install -y libyaml-dev

ADD requirements.txt /buildbot-master/
ADD ci.py /buildbot-master/

RUN echo '    IdentityFile ~/.ssh/id_rsa' >> /etc/ssh/ssh_config
ADD id_rsa /root/.ssh/id_rsa
RUN /bin/bash -l -c "ssh -o \"StrictHostKeyChecking no\" git@github.com || true"

WORKDIR /buildbot-master
RUN pip install -r requirements.txt
WORKDIR /

ADD master.cfg /buildbot-master/master.cfg

EXPOSE 8010
EXPOSE 9989

CMD ["buildbot", "--verbose", "start", "--nodaemon", "/buildbot-master"]
