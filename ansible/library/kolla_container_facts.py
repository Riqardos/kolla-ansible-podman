from podman import ApiConnection, system, images, containers
from podman.domain import volumes
import json
# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.


    
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: kolla_container_facts
short_description: Module for collecting Docker container facts
description:
  - A module targeting at collecting Docker container facts. It is used for
    detecting whether the container is running on host in Kolla.
options:
  api_version:
    description:
      - The version of the api for docker-py to use when contacting docker
    required: False
    type: str
    default: auto
  name:
    description:
      - Name or names of the containers
    required: False
    type: str or list
author: Jeffrey Zhang
'''

EXAMPLES = '''
- hosts: all
  tasks:
    - name: Gather docker facts
      kolla_container_facts:

    - name: Gather glance container facts
      kolla_container_facts:
        name:
          - glance_api
          - glance_registry
'''


def get_podman_client():
    uri = "unix://localhost/var/run/podman/podman.sock"
    return ApiConnection(uri)


def main():
    argument_spec = dict(
        name=dict(required=False, type='list', default=[]),
        api_version=dict(required=False, type='str', default='auto')
    )

    module = AnsibleModule(argument_spec=argument_spec)
    #print("som za modele")
    results = dict(changed=False, _containers=[])
    client = get_podman_client()#(version=module.params.get('api_version'))
    containersList = containers.list_containers(client)
    names = module.params.get('name')
    #names = ['webserver']
    if names and not isinstance(names, list):
        names = [names]
    for container in containersList:
        for container_name in container['Names']:
            # remove '/' prefix character
            #container_name = container_name[1:]
            if names and container_name not in names:
                continue
            results['_containers'].append(container)
            results[container_name] = container
    module.exit_json(**results)
    print(results)


if __name__ == "__main__":
    main()

