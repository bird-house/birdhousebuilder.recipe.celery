# -*- coding: utf-8 -*-

"""
Recipe celery

http://docs.celeryproject.org/en/latest/
"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, supervisor

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "celery.ini"))
templ_celery_cmd = Template(
     "${prefix}/bin/celery worker -A pyramid_celery.celery_app --ini ${prefix}/etc/phoenix.ini")
templ_flower_cmd = Template(
     "${prefix}/bin/celery flower -A pyramid_celery.celery_app --ini ${prefix}/etc/phoenix.ini")

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs Celery with conda and setups the configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = self.options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix
        self.options['program'] = self.options.get('program', self.name)
        self.options['user'] = options.get('user', '')

        self.bin_dir = b_options.get('bin-directory')

    def install(self, update=False):
        installed = []
        installed += list(self.install_conda(update))
        installed += list(self.install_config())
        installed += list(self.install_celery_supervisor(update))
        installed += list(self.install_flower_supervisor(update))
        return installed

    def install_conda(self, update=False):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'celery pyramid_celery flower'})
        if update == True:
            return script.update()
        else:
            return script.install()

    def install_config(self):
        result = templ_config.render(**self.options)

        output = os.path.join(self.prefix, 'etc', 'celery.ini')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_celery_supervisor(self, update=False):
        """
        install supervisor config for celery
        """
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'user': self.options.get('user'),
             'program': self.options.get('program'),
             'command': templ_celery_cmd.render(prefix=self.prefix, bin_dir=self.bin_dir),
             'stopwaitsecs': '30',
             'killasgroup': 'true',
             })
        return script.install(update)

    def install_flower_supervisor(self, update=False):
        """
        install supervisor config for flower
        """
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'user': self.options['user'],
             'program': self.options['program'] + '_monitor',
             'command': templ_flower_cmd.render(prefix=self.prefix, bin_dir=self.bin_dir),
             'stopwaitsecs': '30',
             'killasgroup': 'true',
             })
        return script.install(update)
    
    def update(self):
       return self.install(update=True)

def uninstall(name, options):
    pass

