******************************
birdhousebuilder.recipe.celery
******************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.celery.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.celery
   :alt: Travis Build

.. contents::

Introduction
************

``birdhousebuilder.recipe.celery`` is a `Buildout <http://buildout.org/>`_ recipe to install and configure `Celery <http://www.celeryproject.org/>`_ Distributed Task Queue with `Anaconda <http://www.continuum.io/>`_.
This recipe is used by the `Birdhouse <http://bird-house.github.io/>`_ project. 


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.

It installs the ``celery`` package from a conda channel  in a conda enviroment named ``birdhouse``. The location of the birdhouse environment is ``.conda/envs/birdhouse``. It deploys a `Supervisor <http://supervisord.org/>`_ configuration for Celery in ``~/.conda/envs/birdhouse/etc/supervisor/conf.d/celery.conf``. Supervisor can be started with ``~/.conda/envs/birdhouse/etc/init.d/supervisord start``.

The recipe depends on ``birdhousebuilder.recipe.conda`` and ``birdhousebuilder.recipe.supervisor``.

Supported options
=================

This recipe supports the following options:

**anaconda-home**
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example::

     export ANACONDA_HOME=/opt/anaconda

   Search priority is:

   1. ``anaconda-home`` in ``buildout.cfg``
   2. ``$ANACONDA_HOME``
   3. ``$HOME/anaconda``


Example usage
=============

The following example ``buildout.cfg`` installs Celery with Anaconda and default options:

.. code-block:: ini 

  [buildout]
  parts = celery

  anaconda-home = /home/myself/anaconda

  [celery]
  recipe = birdhousebuilder.recipe.celery

