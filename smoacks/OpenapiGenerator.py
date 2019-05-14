# CreateApiGenerator.py - Creates an object representing a create API
import os
from jinja2 import Environment, Template, FileSystemLoader
import yaml
from smoacks.sconfig import sconfig

class OpenapiGenerator:
    def __init__(self, app_object):
        self._app_object = app_object
        self.name = self._app_object.name

    def getJinjaDict(self):
        # Establish constant values and the overall dictionary structure
        result = {
            'name': self.name,
            'snakeName': self._app_object.getSnakeName(),
            'mixedName': self.name,
            'identitySchemaName': self._app_object.identitySchemaName,
            'extendedSchemaName': self._app_object.extendedSchemaName
        }
        # Loop through the properties and update the structure where needed
        return result

    def render_to_yaml_obj(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('ModelAPIs.jinja')
        result = yaml.load(template.render(self.getJinjaDict()), Loader=yaml.FullLoader)
        return result
