# sconfig.py - smoacks configuration file
import yaml
import logging

LOGGER = logging.getLogger('SMOACKS')

with open('conf/smoacks_default.yaml', 'r') as yamlconfig:
    sconfig = yaml.load(yamlconfig, Loader=yaml.FullLoader)

LOGGER.debug('SMOACKS configuration: {}'.format(str(sconfig)))
