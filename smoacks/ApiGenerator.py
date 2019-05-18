import copy
import os
import logging
import sys
import yaml
from openapi_spec_validator import validate_spec
from smoacks.sconfig import sconfig
from smoacks.Schema import Schema, scr_schemas
from smoacks.AppObject import AppObject, scr_objects
from smoacks.ConnexionApiGenerator import ConnexionApiGenerator
from smoacks.NoseTestGenerator import NoseTestGenerator
from smoacks.OpenapiGenerator import OpenapiGenerator
from smoacks.ServerGenerator import ServerGenerator
from smoacks.SqlAlchemyGenerator import SqlAlchemyGenerator

LOGGER = logging.getLogger('ApiGenerator')


def generate_code():
    SPEC_FILENAME = os.path.join(sconfig['structure']['root'],
                                 sconfig['structure']['specdir'],
                                 sconfig['parameters']['source_spec'])
    LOGGER.info('Generating application from {}'.format(SPEC_FILENAME))

    # Load the configuration yaml file
    try:
        OPENAPI_SPEC = yaml.load(open(SPEC_FILENAME), Loader=yaml.FullLoader)
    except:
        print("Error opening / parsing {}, likely missing, unreadable, nor not YAML".format(SPEC_FILENAME))
        exit(2)

    VALIDATE_COPY = copy.deepcopy(OPENAPI_SPEC)

    # Validate that the provided YAML is an OpenAPI specification
    # For details see https://pypi.org/project/openapi-spec-validator/#description
    try:
        validate_spec(VALIDATE_COPY)
    except:
        print("Specification {} is not a valid OpenAPI 3.0 specification".format(SPEC_FILENAME))
        exit(3)

    # Find where the schema definitions exist in the API spec
    SCHEMAS_YAML = OPENAPI_SPEC['components']['schemas']

    # TODO: Better job handling update vs. identity; better
    #       handling of missing descriptions
    for schema in SCHEMAS_YAML:
        print('Schema: {}'.format(schema))
        # Create the global dictionary of schemas
        scr_schemas[schema] = Schema(schema, SCHEMAS_YAML[schema])
        # If this schema object identifies an AppObject, then create it
        # (if needed), and set the identity object property on it
        objectDesc = scr_schemas[schema].description
        if scr_schemas[schema].identityObject:
            print("--> Identity Object!")
            objectName = scr_schemas[schema].identityObject
            if objectName not in scr_objects:
                scr_objects[objectName] = AppObject(objectName, objectDesc)
            scr_objects[objectName].addSchema(scr_schemas[schema])
        # If this schema object updates an AppObject, then create it
        # (if needed), and set the update object property on it
        if scr_schemas[schema].updateObject:
            objectName = scr_schemas[schema].updateObject
            if objectName not in scr_objects:
                scr_objects[objectName] = AppObject(objectName, objectDesc)
            scr_objects[objectName].addSchema(scr_schemas[schema])
        if scr_schemas[schema].extendedObject:
            objectName = scr_schemas[schema].extendedObject
            if objectName not in scr_objects:
                scr_objects[objectName] = AppObject(objectName, objectDesc)
            scr_objects[objectName].addSchema(scr_schemas[schema])

    # If the parameters say to not include login, remove it from the path output
    if not sconfig['parameters']['include_login']:
        print('Removing /login path')
        OPENAPI_SPEC['paths'].pop('/login')
        OPENAPI_SPEC['components']['schemas'].pop('Login')

    # Generate the schemas
    for object_name in scr_objects:
        print('Handling {}'.format(object_name))
        sqlalchemy_generator = SqlAlchemyGenerator(scr_objects[object_name])
        sqlalchemy_generator.render()
        connexion_generator = ConnexionApiGenerator(scr_objects[object_name])
        connexion_generator.render()
        nosetest_generator = NoseTestGenerator(scr_objects[object_name])
        nosetest_generator.render()
        openapi_generator = OpenapiGenerator(scr_objects[object_name])
        api_obj = openapi_generator.render_to_yaml_obj()
        OPENAPI_SPEC['paths'].update(api_obj)

    server_generator = ServerGenerator(scr_objects)
    server_generator.render()
    filedir = os.path.join(sconfig['structure']['root'], sconfig['structure']['specdir'])
    if not os.path.isdir(filedir):
        os.makedirs(filedir, exist_ok=True)
    outfile = open(os.path.join(filedir, sconfig['parameters']['dest_spec']), "w")
    yaml.dump(OPENAPI_SPEC, outfile, default_flow_style=False)
