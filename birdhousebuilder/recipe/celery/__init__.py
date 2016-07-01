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
from zc.recipe.deployment import Configuration
import birdhousebuilder.recipe.supervisor
import birdhousebuilder.recipe.conda

templ_config_py = Template(filename=os.path.join(os.path.dirname(__file__), "celeryconfig_py"))
templ_celery_cmd = Template(
     "${bin_directory}/celery worker -A ${app} --loglevel=${loglevel}")
templ_flower_cmd = Template(
     "${bin_directory}/celery flower -A ${app} --loglevel=${loglevel}")

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs Celery with conda and setups the configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name
        
        self.logger = logging.getLogger(self.name)

        # deployment layout
        def add_section(section_name, options):
            if section_name in buildout._raw:
                raise KeyError("already in buildout", section_name)
            buildout._raw[section_name] = options
            buildout[section_name] # cause it to be added to the working parts
            
        self.deployment_name = self.name + "-celery-deployment"
        self.deployment = zc.recipe.deployment.Install(buildout, self.deployment_name, {
            'name': "celery",
            'prefix': self.options.get('prefix'),
            'user': self.options.get('user'),
            'etc-user': self.options.get('etc-user')})
        add_section(self.deployment_name, self.deployment.options)

        self.options['user'] = self.deployment.options['user']
        self.options['etc-user'] = self.deployment.options['etc-user']
        self.options['etc-prefix'] = self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = self.deployment.options['etc-directory']
        self.options['log-directory'] = self.options['log_directory'] = self.deployment.options['log-directory']
        self.options['run-directory'] = self.options['run_directory'] = self.deployment.options['run-directory']
        self.options['cache-directory'] = self.options['cache_directory'] = self.deployment.options['cache-directory']
        self.options['bin-directory'] = self.options['bin_directory'] = b_options['bin-directory']
        self.prefix = self.options['prefix']

        # conda environment path
        self.options['env'] = self.options.get('env', '')
        self.options['pkgs'] = self.options.get('pkgs', 'celery redis-py pymongo')
        self.options['channels'] = self.options.get('channels', 'defaults birdhouse')
        
        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {
            #'prefix': self.options.get('conda-prefix', ''),
            'env': self.options['env'],
            'pkgs': self.options['pkgs'],
            'channels': self.options['channels']})
        self.options['conda-prefix'] = self.options['conda_prefix'] = self.conda.options['prefix']
        
        # celery options
        self.options['app'] = options.get('app', 'myapp')
        self.use_celeryconfig = bool_option(self.options, 'use-celeryconfig', True)
        self.options['broker-url'] = self.options.get('broker-url', 'redis://localhost:6379/0')
        self.options['celery-result-backend'] = self.options.get('celery-result-backend', 'redis://localhost:6379/0')
        self.options['loglevel'] = self.options.get('loglevel', 'WARNING')

    def install(self, update=False):
        installed = []
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_script())
        if self.use_celeryconfig:
            installed += list(self.install_config_py())
        installed += list(self.install_celery_supervisor(update))
        return installed

    def install_script(self):
        eggs = ['celery']
        if 'redis://' in self.options['broker-url']:
            eggs.append('redis')
        elif 'mongodb://' in self.options['broker-url']:
            eggs.append('pymongo')
        if 'eggs' in self.options:
            eggs = eggs + self.options['eggs'].split()
        celery_egg_options = {
            'eggs': '\n'.join(eggs),
            'extra-paths': self.options['etc-directory'],
            #'entry-points': 'celery=celery.__main__:main',
            'scripts': 'celery=celery'}
       
        celery_egg = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            celery_egg_options,
        )
        return list(celery_egg.install())
        
    def install_config_py(self):
        text = templ_config_py.render(options=self.options)
        config = Configuration(self.buildout, 'celeryconfig.py', {
            'deployment': self.deployment_name,
            'text': text})
        return [config.install()]

    def install_celery_supervisor(self, update=False):
        """
        install supervisor config for celery
        """
        script = birdhousebuilder.recipe.supervisor.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'etc-user': self.options.get('etc-user'),
             'program': self.name,
             'command': templ_celery_cmd.render(**self.options),
             'stopwaitsecs': '30',
             'killasgroup': 'true',
             })
        return script.install(update)
    
    def update(self):
       return self.install(update=True)

def uninstall(name, options):
    pass

