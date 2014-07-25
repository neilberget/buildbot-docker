To try make sure you have [docker](http://boot2docker.io/) installed, then copy your github private key id\_rsa into both the buildbot-master and buildbot-slave folders, then:

    cd buildbot-master
    ./run.sh

In another terminal:

    cd buildbot-slave
    ./run.sh

Then visit http://docker\_host:8010

Adding repos
----

* Ensure the repo has a .build.yml file in the root of the repo.
* In buildbot-master/master.cfg: add the repo to the github\_repos array.

.build.yml
----
The .build.yml should follow the following format:

    environment:
      services:
        mysql:
          linked_name: mysql
          env:
            MYSQL_ROOT_PASSWORD: root

    build:
      test:
        - bundle exec rake db:create db:test:prepare
        - bundle exec rake db:migrate RAILS_ENV=test
        - bundle exec rspec --fail-fast spec
      assets:
        - bundle exec rake assets:precompile

    publish:
      repository: registry.edmodo.io
      name: snapshot

### Environment
The environment section should specify all the 3rd party services that this build depends on such as mysql or mongo.

Each entry under the services entry will cause a docker run to execute for that named image.

The optional linked\_name parameter specifies what this container will be named via the --link switch when the build container is run.

The optional env section specifies any environment variables that need to be set for the run.

### Build
The build specifies a series of steps that need to be run to execute a build. 
Typically this will be a run of the unit tests, followed by asset compilation.

The build steps will be run in top down order and if any fail the subsequent steps will not be attempted.

The key names under build can be set to whatever you'd like and are just used for display purposes.

The array of steps under each key name will be run in the same container, but the steps in separate keys will be run in a fresh container.
In the example above, the 3 test files will be run in the same container and if they succeed, the assets step will be run in the context of a new container.        

### Publish
If the build steps all pass, the docker image will be pushed to the repository/name specified here.

