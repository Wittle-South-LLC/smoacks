from setuptools import setup

setup(name='smoacks',
      version='0.1.7',
      description='Simple Microservices with OpenAPI, Connexion, Kubernetes, and SQLAlchemy',
      url='https://github.com/wittlesouth/smoacks',
      author='Wittle South Ventures, LLC',
      author_email='service@wittlesouth.com',
      license='MIT',
      packages=['smoacks'],
      include_package_data=True,
      data_files=[('conf', ['conf/smoacks_default.yaml']),
                  ('templates', ['templates/app-env.jinja',
                                 'templates/dev-api-server.jinja',
                                 'templates/server-loop.jinja',
                                 'templates/requirements.jinja',
                                 'templates/Dockerfile.jinja',
                                 'templates/server_logging.jinja',
                                 'templates/schema.jinja',
                                 'templates/ConnexionApis.jinja',
                                 'templates/ModelApis.jinja',
                                 'templates/server.jinja',
                                 'templates/SQLAlchemyModel.jinja'])],
      install_requires=[
          'jinja2',
          'PyYAML'
      ],
      entry_points={
          'console_scripts': ['smoacks-setup=smoacks.command_line:main',
                              'smoacks-gen=smoacks.command_line:gen']
      },
      zip_safe=False)
