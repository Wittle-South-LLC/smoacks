# sconfig.py - smoacks configuration file
import os
import yaml
import logging

structure_overrides = ['SMOACKS_ROOT']
parameters_overrides = ['SMOACKS_SOURCE_SPEC', 'SMOACKS_DEST_SPEC',
                        'SMOACKS_SERVER_CONTAINER_PORT']
env_defaults_overrides = ['SMOACKS_APP_NAME']

LOGGER = logging.getLogger('SMOACKS')

with open('conf/smoacks_default.yaml', 'r') as yamlconfig:
    sconfig = yaml.load(yamlconfig, Loader=yaml.FullLoader)

    for ovr in structure_overrides:
        if ovr in os.environ:
            sconfig['structure'][ovr[8:].lower()] = os.environ[ovr]
    for ovr in parameters_overrides:
        if ovr in os.environ:
            sconfig['parameters'][ovr[8:].lower()] = os.environ[ovr]
    for ovr in env_defaults_overrides:
        if ovr in os.environ:
            sconfig['env_defaults'][ovr.lower()] = os.environ[ovr]
    sconfig['env_defaults']['smoacks_app_name_c'] = sconfig['env_defaults']['smoacks_app_name'].upper()
    sconfig['env_defaults']['smoacks_app_name_k'] = sconfig['env_defaults']['smoacks_app_name'].replace('_', '-')
    # Promote spec name from parameters into env defaults so it can more easily
    # be used in jinja templates during generation
    sconfig['env_defaults']['dest_spec'] = sconfig['parameters']['dest_spec']
#    if 'SMOACKS_ROOT' in os.environ:
#        sconfig['structure']['root'] = os.environ['SMOACKS_ROOT']
LOGGER.debug('SMOACKS configuration: {}'.format(str(sconfig)))
