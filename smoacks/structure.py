# structure.py - Routines for generation app structure
import os
import stat
from jinja2 import Environment, Template, TemplateError, UndefinedError, TemplateNotFound, FileSystemLoader
from smoacks.sconfig import sconfig

class SmoacksStructure:
    def __init__(self):
        self.name = 'SmoacksStructure'
        self.env = [
            {'template': 'app-env.jinja',
             'dir': sconfig['structure']['bindir'],
             'outfile': "app-env"},
            {'template': 'base.jinja',
             'dir': sconfig['structure']['datamodeldir'],
             'outfile': 'base.py'},
            {'template': 'dev-api-server.jinja',
             'dir': sconfig['structure']['kubedir'],
             'outfile': "dev-api-server.yaml"},
            {'template': 'Dockerfile.jinja',
             'dir': sconfig['structure']['sourcedir'],
             'outfile': "Dockerfile"},
            {'template': 'local-env.jinja',
             'dir': sconfig['structure']['bindir'],
             'outfile': "local-env"},
            {'template': 'schema.jinja',
             'dir': sconfig['structure']['specdir'],
             'outfile': sconfig['parameters']['source_spec']},
            {'template': 'server-loop.jinja',
             'dir': sconfig['structure']['sourcedir'],
             'outfile': "server-loop",
             'executable': True},
            {'template': 'server_logging.jinja',
             'dir': sconfig['structure']['sourcedir'],
             'outfile': "server_logging.yaml"},
            {'template': 'server.jinja',
             'dir': sconfig['structure']['sourcedir'],
             'outfile': "server.py"},
            {'template': 'shutdown.jinja',
             'dir': sconfig['structure']['apiobjectdir'],
             'outfile': "shutdown.py"},
            {'template': 'test-api-server.jinja',
             'dir': sconfig['structure']['kubedir'],
             'outfile': "test-api-server.yaml"},
            {'template': 'testme.jinja',
             'dir': sconfig['structure']['bindir'],
             'outfile': 'testme',
             'executable': True},
            {'template': 'TestUtil.jinja',
             'dir': sconfig['structure']['testdir'],
             'outfile': 'TestUtil.py'}
        ]
        self.template_dict = sconfig['env_defaults']
        self.template_dict['smoacks_local_dev_path'] = os.getcwd()

    def renderEnvironment(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        # Ensure there is a coverage directory with a runType.bash in it
        if not os.path.isdir('coverage'):
              coverpath = os.path.join(sconfig['structure']['root'], 'coverage')
              os.makedirs(coverpath, exist_ok=True)
              rtfile = open(os.path.join(coverpath, 'runType.bash'), "w")
              rtfile.write('export run_coverage=0')
              rtfile.close()
        for filespec in self.env:
           template = env.get_template(filespec['template'])
           filedir = os.path.join(sconfig['structure']['root'], filespec['dir']) if filespec['dir'] else sconfig['structure']['root']
           if not os.path.isdir(filedir):
              os.makedirs(filedir, exist_ok=True)
           outfile = open(os.path.join(filedir, filespec['outfile']), "w")
           try:
               filestring = template.render(self.template_dict)
               outfile.write(filestring)
               if 'executable' in filespec and filespec['executable']:
                   perm = os.stat(os.path.join(filedir, filespec['outfile']))
                   os.chmod(os.path.join(filedir, filespec['outfile']), perm.st_mode | stat.S_IEXEC)
               outfile.close() 
           except TemplateNotFound:
               print('Caught a TemplateNotFoundError on {}'.format(filespec['template']))
           except UndefinedError:
               print('Caught a UndefinedError on {}'.format(filespec['template']))
           except TemplateError:
               print('Caught a TemplateError on {}'.format(filespec['template']))
           except:
               print('Caught an untyped error on {}'.format(filespec['template']))