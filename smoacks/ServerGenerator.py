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
            'dmImports': [],
            'gensubdir': sconfig['structure']['gensubdir']
        }
        # Loop through the properties and update the structure where needed
        set_first_table = False
        for objName in self._app_objects:
            result['dmImports'].append(self.get_import(self._app_objects[objName]))
            if not set_first_table:
                set_first_table = True
                result['first_table_name'] = objName
        return result

    def render(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('DataModel.jinja')
        filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['datamodeldir'])
        tmf_file_name = os.path.join(filedir, '__init__.py') 
        if not os.path.isfile(tmf_file_name):
            tmf_file = open(tmf_file_name, "w")
            tmf_file.close()
        outfile = open(os.path.join(filedir, 'DataModel.py'), "w")
        outfile.write(template.render(self.getJinjaDict()))
