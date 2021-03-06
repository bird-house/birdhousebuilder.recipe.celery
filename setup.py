# -*- coding: utf-8 -*-
"""
This module contains the tool of birdhousebuilder.recipe.celery
"""
from setuptools import find_packages
from setuptools import setup

name = 'birdhousebuilder.recipe.celery'

version = '0.2.0'
description = 'A Buildout recipe to install and configure Celery for Birdhouse.'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

entry_points = '''
[zc.buildout]
default = %(name)s:Recipe
[zc.buildout.uninstall]
default = %(name)s:uninstall
''' % globals()

reqs = ['setuptools', 'zc.buildout',
        'pyyaml',
        'zc.recipe.egg',
        'zc.recipe.deployment',
        'Mako',
        'birdhousebuilder.recipe.conda',
        'birdhousebuilder.recipe.supervisor',]
tests_reqs = ['zc.buildout', 'zope.testing']

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
      keywords='buildout recipe birdhouse conda celery',
      author='Birdhouse',
      author_email="wps-dev at dkrz.de",
      url='https://github.com/bird-house/birdhousebuilder.recipe.celery',
      license='Apache License 2',
      install_requires = reqs,
      extras_require = dict(tests=tests_reqs),
      entry_points = entry_points,
      packages = find_packages(exclude=['ez_setup']),
      namespace_packages = ['birdhousebuilder', 'birdhousebuilder.recipe'],
      include_package_data = True,
      zip_safe = False,
      )
