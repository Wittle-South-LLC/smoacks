# CreateApiGenerator.py - Creates an object representing a create API
import os
from jinja2 import Environment, Template, FileSystemLoader
from smoacks.sconfig import sconfig

class SqlAlchemyGenerator:
    def __init__(self, app_object):
        self._app_object = app_object
        self.name = self._app_object.name

    def getField(self, prop):
        if prop.type == 'string':
            if prop.isId:
                return "{} = Column(BINARY(16), primary_key=True)"
            elif prop.format == 'date':
                return "{} = Column(DateTime)".format(prop.name)
            elif prop.maxLength and prop.maxLength > 0:
                return "{} = Column(String({}))".format(prop.name, prop.maxLength)
            else:
                return "{} = Column(String(80))".format(prop.name)
        elif prop.type == 'number':
            if prop.format == 'double':
                return "{} = Column(Double)".format(prop.name)
            else:
                return "{} = Column(Float)".format(prop.name)
        elif prop.type == 'integer':
            if prop.format == 'int64':
                return "{} = Column(Long)".format(prop.name)
            else:
                return "{} = Column(Integer)".format(prop.name)
        elif prop.type == 'object':
            return "{} = Column(JSON)"
        else:
            raise ValueError("Property {} has invalid type {}".format(prop.name, prop.type))

    def getJinjaDict(self):
        # Establish constant values and the overall dictionary structure
        result = {
            'name': self.name,
            'snakeName': self._app_object.getSnakeName(),
            'mixedName': self.name,
            'dmFields': []
        }
        # Loop through the properties and update the structure where needed
        properties = self._app_object.getAllProperties()
        for prop in properties:
            if not prop.isId and not (prop.name in ['record_created', 'record_updated']):
                result['dmFields'].append(self.getField(prop))
        return result

    def render(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('SQLAlchemyModel.jinja')
        filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['datamodeldir'])
        if not os.path.isdir(filedir):
            os.makedirs(filedir, exist_ok=True)
        outfile = open(os.path.join(filedir, "{}.py".format(self.name)), "w")
        outfile.write(template.render(self.getJinjaDict()))
