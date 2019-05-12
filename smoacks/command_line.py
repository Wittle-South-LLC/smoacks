from smoacks.sconfig import sconfig
from smoacks.structure import SmoacksStructure

def main():
    my_struct = SmoacksStructure()
    print ('Setting up SMOACKS for this project with bindir: {}'.format(sconfig['structure']['bindir']))
    my_struct.renderEnvFile()
    