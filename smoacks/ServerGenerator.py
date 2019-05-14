# ServerGenerator.py - Creates an object implementing a Connexion API
import os
from jinja2 import Environment, Template, FileSystemLoader
from smoacks.sconfig import sconfig

class ServerGenerator:
    def __init__(self, app_objects):
        self._app_objects = app_objects

    def get_import(self, app_object):
        return "from dm.{} import {}".format(app_object.name, app_object.name)

    def getJinjaDict(self):
        # Establish constant values and the overall dictionary structure
        result = {
            'dmImports': []
        }
        # Loop through the properties and update the structure where needed
        for objName in self._app_objects:
            result['dmImports'].append(self.get_import(self._app_objects[objName]))
        return result

    def render(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('server.jinja')
        filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['sourcedir'])
        if not os.path.isdir(filedir):
            os.makedirs(filedir, exist_ok=True)
        outfile = open(os.path.join(filedir, 'server.py'), "w")
        outfile.write(template.render(self.getJinjaDict()))
