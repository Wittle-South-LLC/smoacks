# sconfig.py - smoacks configuration file
import os
import yaml
import logging

LOGGER = logging.getLogger('SMOACKS')

with open('conf/smoacks_default.yaml', 'r') as yamlconfig:
    sconfig = yaml.load(yamlconfig, Loader=yaml.FullLoader)

    if 'SMOACKS_ROOT' in os.environ:
        sconfig['structure']['root'] = os.environ['SMOACKS_ROOT']

LOGGER.debug('SMOACKS configuration: {}'.format(str(sconfig)))
