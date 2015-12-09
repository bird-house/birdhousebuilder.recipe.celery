# -*- coding: utf-8 -*-

"""
Recipe celery

http://docs.celeryproject.org/en/latest/
"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, supervisor

config = Template(filename=os.path.join(os.path.dirname(__file__), "celery.ini"))

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs Celery with conda and setups the configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = self.options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix

    def install(self, update=False):
        installed = []
        installed += list(self.install_conda(update))
        installed += list(self.install_config())
        return installed

    def install_conda(self, update=False):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'celery'})
        if update == True:
            return script.update()
        else:
            return script.install()

    def install_config(self):
        result = config.render(**self.options)

        output = os.path.join(self.prefix, 'etc', 'celery.ini')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def update(self):
       return self.install(update=True)

def uninstall(name, options):
    pass

