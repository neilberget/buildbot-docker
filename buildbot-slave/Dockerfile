FROM ubuntu:12.04

RUN apt-get update

RUN apt-get install -y python-setuptools
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y git-core
RUN apt-get install -y curl
RUN apt-get install -y python-pip

RUN curl https://get.docker.io/builds/Linux/x86_64/docker-latest -o /usr/local/bin/docker
RUN chmod +x /usr/local/bin/docker

RUN easy_install buildbot-slave

RUN mkdir /buildbot-slave
ADD requirements.txt /buildbot-slave/
ADD ci.py /buildbot-slave/
ADD start_slave.sh /buildbot-slave/start_slave.sh

WORKDIR /buildbot-slave
RUN pip install -r requirements.txt

RUN echo '    IdentityFile ~/.ssh/id_rsa' >> /etc/ssh/ssh_config
RUN /bin/bash -l -c "ssh -o \"StrictHostKeyChecking no\" git@github.com || true"


ADD id_rsa /root/.ssh/id_rsa

WORKDIR /buildbot-slave

CMD ["./start_slave.sh"]
