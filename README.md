# smoacks
Simple Microservices with OpenAPI, Connexion, Kubernetes, and SQLAlchemy

This library will generate a microservice application intended for deployment
in a Kubernetes environment, based on an OpenAPI 3.0 schema. It will work
from the schema to create API endpoints and a SQLAlchemy data model.

Deployment Dependencies for Generated Code

- Flask for HTTP request handling
- Connexion for RESTful API validation & routing
- SQLAlchemy for database persistence

Dependencies in development for generating code
- Jinja2 for code generation from internal templates; not at runtime
- PyYAML for configuration file; 
