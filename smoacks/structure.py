# structure.py - Routines for generation app structure
import os
from jinja2 import Environment, Template, FileSystemLoader
from smoacks.sconfig import sconfig

class SmoacksStructure:
    def __init__(self):
        self.name = 'SmoacksStructure'

    def getEnvDict(self):
        result = sconfig['env_defaults']
        return result

    def renderEnvFile(self):
        env = Environment(
            loader = FileSystemLoader('templates')
        )
        template = env.get_template('app-env.jinja')
        if not os.path.isdir(sconfig['structure']['bindir']):
            os.makedirs(sconfig['structure']['bindir'], exist_ok=True)
        outfile = open(sconfig['structure']['bindir'] + "/app-env", "w")
        outfile.write(template.render(self.getEnvDict()))
