# NoseTestGenerator.py - Creates nose tests for a model API
import os
from jinja2 import Environment, Template, FileSystemLoader
from smoacks.sconfig import sconfig

class NoseTestGenerator:
    def __init__(self, app_object):
        self._app_object = app_object
        self.name = self._app_object.name

    def getCreateObject(self):
        # Loop through the properties and update the structure where needed
        result = {}
        properties = self._app_object.getAllProperties()
        for prop in properties:
            if not prop.isId:
                result[prop.name] = prop.example
        return result

    def getJinjaDict(self):
        # Establish constant values and the overall dictionary structure
        result = {
            'name': self.name,
            'snakeName': self._app_object.getSnakeName(),
            'createObj': self.getCreateObject()
        }
        properties = self._app_object.getAllProperties()
        getAsserts = []
        unitTestEditObject = {}
        unitTestAssert = None
        for prop in properties:
            if prop.isId:
                result['name_id'] = prop.name
            # We need to change a value in unit tests of PUT verb
            elif prop.example:
                if prop.editUnitTest:
                    unitTestEditObject[prop.name] = prop.editUnitTest
                    unitTestAssert = 'assert json["{}"] == {}'.format(prop.name, prop.getUnitTestLiteral())
                else:
                    unitTestEditObject[prop.name] = prop.example
                    getAsserts.append('assert json["{}"] == {}'.format(prop.name, prop.getExamplePythonLiteral()))
        result['getAsserts'] = getAsserts
        result['unitTestEditObject'] = str(unitTestEditObject)
        result['unitTestAssert'] = unitTestAssert
        return result

    def render(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('NoseTests.jinja')
        filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['testdir'])
        if not os.path.isdir(filedir):
            os.makedirs(filedir, exist_ok=True)
        outfile = open(os.path.join(filedir, "test-{}-api.py".format(self._app_object.getSnakeName())), "w")
        outfile.write(template.render(self.getJinjaDict()))
