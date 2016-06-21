# -*- coding: utf-8 -*-

"""
Recipe celery:

* http://docs.celeryproject.org/en/latest/
* https://github.com/collective/collective.recipe.celery
"""

import os
from mako.template import Template
import logging

from zc.buildout.buildout import bool_option
import zc.buildout
import zc.recipe.egg
import zc.recipe.deployment
from birdhousebuilder.recipe import conda, supervisor

templ_config_py = Template(filename=os.path.join(os.path.dirname(__file__), "celeryconfig_py"))
templ_celery_cmd = Template(
     "${bin_dir}/celery worker -A ${app} --loglevel=${loglevel}")
templ_flower_cmd = Template(
     "${bin_dir}/celery flower -A ${app} --loglevel=${loglevel}")

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs Celery with conda and setups the configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.options['name'] = self.options.get('name', self.name)
        self.name = self.options['name']

        self.logger = logging.getLogger(name)

        deployment = zc.recipe.deployment.Install(buildout, 'celery', {
                                                'prefix': self.options['prefix'],
                                                'user': self.options['user'],
                                                'etc-user': self.options['user']})
        deployment.install()
        
        self.options['etc-prefix'] = deployment.options['etc-prefix']
        self.options['var-prefix'] = deployment.options['var-prefix']
        self.options['etc-directory'] = deployment.options['etc-directory']
        self.options['lib-directory'] = deployment.options['lib-directory']
        self.options['log-directory'] = deployment.options['log-directory']
        self.options['cache-directory'] = deployment.options['cache-directory']
        self.prefix = self.options['prefix']

        self.options['user'] = options.get('user', '')
        self.options['app'] = options.get('app', 'myapp')
        self.use_monitor = bool_option(self.options, 'use-monitor', False)
        self.use_celeryconfig = bool_option(self.options, 'use-celeryconfig', True)
        self.options['broker-url'] = self.options.get('broker-url', 'redis://localhost:6379/0')
        self.options['celery-result-backend'] = self.options.get('celery-result-backend', 'redis://localhost:6379/0')
        self.options['loglevel'] = self.options.get('loglevel', 'WARNING')
        self.conf_filename = os.path.join(self.options['etc-directory'], 'celeryconfig.py')

        self.bin_dir = b_options.get('bin-directory')
        self.options['bin_dir'] = self.bin_dir

    def install(self, update=False):
        installed = []
        installed += list(self.install_conda(update))
        installed += list(self.install_script())
        if self.use_celeryconfig:
            installed += list(self.install_config_py())
        installed += list(self.install_celery_supervisor(update))
        if self.use_monitor:
            installed += list(self.install_flower_supervisor(update))
        return installed

    def install_conda(self, update=False):
        pkgs = ['celery']
        if self.use_monitor:
            pkgs.append('flower')
        if 'redis://' in self.options['broker-url']:
            pkgs.append('redis-py')
        elif 'mongodb://' in self.options['broker-url']:
            pkgs.append('pymongo')
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': ' '.join(pkgs)})
        return script.install(update=update)

    def install_script(self):
        eggs = ['celery']
        if self.use_monitor:
            eggs.append('flower')
        if 'redis://' in self.options['broker-url']:
            eggs.append('redis')
        elif 'mongodb://' in self.options['broker-url']:
            eggs.append('pymongo')
        if 'eggs' in self.options:
            eggs = eggs + self.options['eggs'].split()
        celery_egg_options = {
            'eggs': '\n'.join(eggs),
            'extra-paths': os.path.dirname(self.conf_filename),
            #'entry-points': 'celery=celery.__main__:main',
            'scripts': 'celery=celery'}
       
        celery_egg = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            celery_egg_options,
        )
        return list(celery_egg.install())
        
    def install_config_py(self):
        result = templ_config_py.render(options=self.options)
        output = self.conf_filename

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
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'program': self.name,
             'command': templ_celery_cmd.render(**self.options),
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
            {'prefix': self.options['prefix'],
             'user': self.options['user'],
             'program': self.name + '_monitor',
             'command': templ_flower_cmd.render(**self.options),
             'stopwaitsecs': '30',
             'killasgroup': 'true',
             })
        return script.install(update)
    
    def update(self):
       return self.install(update=True)

def uninstall(name, options):
    pass

