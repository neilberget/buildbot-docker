from awesome_print import ap
import sys
from subprocess import call
import uuid
import yaml

class CI:
  def __init__(self, buildfile, build_id=None):
    self.rules = self.parse_buildfile(buildfile)
    self.build_id = build_id if build_id != None else str(uuid.uuid4())

  def parse_buildfile(self, buildfile):
    stream = open(buildfile, 'r')

    return yaml.load(stream)

  def build_tag(self):
    return 'build-' + self.build_id

  def build_dockerfile(self):
    # copy private key into build
    self.prepare_key()

    build_tag = self.build_tag()
    build_cmd = 'docker build -t %(build_tag)s .' % locals()
    ap(build_cmd)
    return call(build_cmd.split())

  def prepare_key(self):
    key_cmd = 'cp --preserve /root/.ssh/id_rsa .'
    call(key_cmd.split())

  def load_environment(self):
    for image, service_config in self.services().iteritems():
      container_name = self.container_name_for_service(image, service_config)

      envs = ''
      if service_config and 'env' in service_config:
        envs = self.envs(service_config['env'])

      run_cmd = 'docker run -d %(envs)s --name %(container_name)s %(image)s' % locals()
      ap(run_cmd)
      result = call(run_cmd.split())
      if result > 0:
        return result

    return 0

  def unload_environment(self):
    for image, service_config in self.services().iteritems():
      container_name = self.container_name_for_service(image, service_config)

      stop_cmd = 'docker stop %(container_name)s' % locals()
      ap(stop_cmd)
      call(stop_cmd.split())

      rm_cmd = 'docker rm %(container_name)s' % locals()
      ap(rm_cmd)
      call(rm_cmd.split())

  def container_name_for_service(self, default, service_config):
    container_name = default

    if service_config and 'linked_name' in service_config:
      container_name = service_config['linked_name']

    return container_name + "-" + self.build_id

  def envs(self, env_dict):
    single_env = lambda k, v: "-e " + k + "=" + v

    return " ".join([single_env(a,b) for (a,b) in env_dict.items()])

  def run_build_steps(self):
    build_tag = self.build_tag()

    for step, cmds in self.build_steps().items():
      ap(step)
      all_cmds = ' && '.join(cmds)
      all_cmds = '/bin/bash -l -c "%(all_cmds)s"' % locals()
      links = self.service_links()

      build_run_cmd = 'docker run -i %(links)s %(build_tag)s %(all_cmds)s' % locals()
      ap(build_run_cmd)

      result = call(build_run_cmd, shell=True)
      ap(result)

      if result != 0:
        return result

    return 0

  def publish(self):
    if not 'publish' in self.rules:
      return

    publish_rules = self.rules['publish']

    if not 'repository' in publish_rules or not 'name' in publish_rules:
      ap("Nowhere to publish..")
      return 1

    build_tag  = self.build_tag()
    repository = publish_rules['repository']
    name       = publish_rules['name']

    ap("Tagging")
    tag_cmd = 'docker tag %(build_tag)s %(repository)s/%(name)s' % locals()
    ap(tag_cmd)
    tag_result = call(tag_cmd.split())
    if tag_result > 0:
      return tag_result

    ap("Publishing")
    publish_cmd = 'docker push %(repository)s/%(name)s' % locals()
    ap(publish_cmd)
    return call(publish_cmd.split())


  def service_links(self):
    output = ''
    for image, service_config in self.services().iteritems():
      container_name = self.container_name_for_service(image, service_config)

      linked_name = image
      if service_config and 'linked_name' in service_config:
        linked_name = service_config['linked_name']

      output = output + '--link %(container_name)s:%(linked_name)s ' % locals()

    return output

  def services(self):
    services = []

    if 'environment' in self.rules:
      if 'services' in self.rules['environment']:
        services = self.rules['environment']['services']

    return services

  def build_steps(self):
    return self.rules['build']


def main():
  command = sys.argv[1] if len(sys.argv) > 1 else "all"
  build_id = sys.argv[2] if len(sys.argv) > 2 else None
  buildfile = sys.argv[3] if len(sys.argv) > 3 else ".build.yml"

  ci = CI(buildfile, build_id)
  if command == 'all':
    ci.build_dockerfile()
    ci.load_environment()
    if ci.run_build_steps() == 0:
      ci.publish()
    # ci.notify()
    ci.unload_environment()
  elif command == 'build':
    sys.exit(ci.build_dockerfile())
  elif command == 'load_environment':
    sys.exit(ci.load_environment())
  elif command == 'run_build':
    sys.exit(ci.run_build_steps())
  elif command == 'publish':
    sys.exit(ci.publish())
  elif command == 'unload_environment':
    sys.exit(ci.unload_environment())


if __name__ == "__main__":
    main()
