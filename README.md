# smoacks
Simple Microservices with OpenAPI, Connexion, Kubernetes, and SQLAlchemy

This library will generate a microservice application intended for deployment
in a Kubernetes environment, based on an OpenAPI 3.0 schema. It will work
from the schema to create API endpoints and a SQLAlchemy data model.

The microservice application will include a set of scripts to set up
environment variables used by the application, yaml files to deploy the
application as a container, a Dockerfile to package the service as a container,
as well as generated source files. See [development environment](https://github.com/Wittle-South-LLC/smoacks/blob/master/DEV_ENVIRONMENT.md)
for an explanation of the development environment assumptions.

## Deployment Dependencies for Generated Code

- Flask for HTTP request handling
- flask_jwt_extended for securing API endpoints
- Connexion for RESTful API validation & routing
- SQLAlchemy for database persistence

### Dependencies in development for generating code
- Jinja2 for code generation from internal templates; not at runtime
- PyYAML for configuration file; 

## Specialized SMOACKS tags for OpenAPI 3.0 specs

The following tags have special meanings for SMOACKS application generation

### Data Model Object Tags
- Schema Tags
    - **x-smoacks-create** - String naming a data model object to be created from
      the schema object to which this tag is attached
    - **x-smoacks-extended** - String naming a data model object that the schema
      object to which this tag is attached should extend with additional attributes
      beyond those provided in the schema tagged with x-smoacks-create
    - **x-smoacks-fk-relationships** - Defines SQLAlchemy relationships to create
      for the data model object. This is a structure that provides the relationship
      name, table, field, and optionally a cascade setting.
    - **x-smoacks-api-verb-param** - Identifies a schema object that should be the
      parameter for an API verb for the object specified by **x-smoacks-object**
      on the same schema. Applies only to POST, SEARCH, GET, PUT verbs.
    - **x-smoacks-api-verb-resp** - Identifies a schema object that should be the
      response for an API verb for the object specified by **x-smoacks-object**
      on the same schema. Applies only to SEARCH and GET verbs.
    - **x-smoacks-object** - Identifies the data model object associated with a
      schema. Ignored if **x-smoacks-create** or **x-smoacks-extended** is attached
      to the same schema. 
- Property Tags
    - **x-smoacks-model-id** - Boolean flagging a property in the schema as the
      primary key for the data model object set in the schema
    - **x-smoacks-foreign-key** - String identifying the table to which this
      property is a foreign key

### Code Generation Hint Tags
- **x-smoacks-search-field:** - Boolean flagging a field in the model as being
  the one that the default search API implementation should query against 
- **x-smoacks-edit-unit-test:** - Identifies field to be changed during unit
  testing of edit API, value replaces example for the property with this tag
- **x-smoacks-test-data** - Flag to identify whether test data should be
  generated for this object (This likely shouldn't be a smoacks attribute,
  I think it is only used by openapi-rim-app)

Version History
---------------

* 0.2.7 - Support cascading database operations on relationships
* 0.2.6 - Support for assigning custom schemas to specific verbs
* 0.2.5 - Support for hydration endpoint
* 0.2.4 - Support for model relationships
* 0.2.3 - Unit test coverage for all generated endpoints
* 0.2.2 - Allows customization of data model and API objects
* 0.2.1 - Supports unit testing authenticated endpoints
* 0.2.0 - First version generating structure, code, and working unit test
* 0.1.X Series - Incremental steps to first working version

