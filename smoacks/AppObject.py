# AppObject.py - Application objects
from smoacks.util import to_camelcase, to_mixedcase, to_snakecase

scr_objects = dict()

class AppObject:
    def __init__(self, name, desc = None):
        self.name = name
        self.description = desc if desc else name
        self._schemas = []
        self._properties = []
        self.identitySchemaName = None
        self.extendedSchemaName = None
        self.emitTestData = False
    
    def addSchema(self, schema):
        self._schemas.append(schema)
        if schema.identityObject:
            self.identitySchemaName = schema.name
            for prop in schema.getProperties().values():
                self._properties.append(prop)
        if schema.extendedObject:
            self.extendedSchemaName = schema.name
    
    def getSnakeName(self):
        return to_snakecase(self.name)
    
    def getCamelName(self):
        return to_camelcase(self.name)
    
    def getMixedName(self):
        return to_mixedcase(self.name)

    def getAllProperties(self):
        return self._properties
