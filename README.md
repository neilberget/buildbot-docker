To try make sure you have [docker](http://boot2docker.io/) installed, then copy your github private key id\_rsa into both the buildbot-master and buildbot-slave folders, then:

    cd buildbot-master
    ./run.sh

In another terminal:

    cd buildbot-slave
    ./run.sh

Then visit http://docker\_host:8010
