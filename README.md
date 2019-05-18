# smoacks
Simple Microservices with OpenAPI, Connexion, Kubernetes, and SQLAlchemy

This library will generate a microservice application intended for deployment
in a Kubernetes environment, based on an OpenAPI 3.0 schema. It will work
from the schema to create API endpoints and a SQLAlchemy data model.

The microservice application will include a set of scripts to set up
environment variables used by the application, yaml files to deploy the
application as a container, a Dockerfile to package the service as a container,
as well as generated source files. See [development environment](DEV_ENVIRONMENT.md)
for an explanation of the development environment assumptions.

Deployment Dependencies for Generated Code

- Flask for HTTP request handling
- flask_jwt_extended for securing API endpoints
- Connexion for RESTful API validation & routing
- SQLAlchemy for database persistence

Dependencies in development for generating code
- Jinja2 for code generation from internal templates; not at runtime
- PyYAML for configuration file; 
