******************************
birdhousebuilder.recipe.celery
******************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.celery.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.celery
   :alt: Travis Build

Introduction
************

``birdhousebuilder.recipe.celery`` is a `Buildout`_ recipe to install and configure `Celery`_ Distributed Task Queue with `Anaconda`_.
This recipe is used by the `Birdhouse`_ project. 

The recipe is based on `collective.recipe.celery <https://pypi.python.org/pypi/collective.recipe.celery>`_.


.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://www.continuum.io/
.. _`Birdhouse`: http://bird-house.github.io/
.. _`Celery`: http://www.celeryproject.org/
.. _`Supervisor`: http://supervisord.org/

Usage
*****

The recipe requires that Anaconda is already installed. You can use the buildout option ``anaconda-home`` to set the prefix for the anaconda installation. Otherwise the environment variable ``CONDA_PREFIX`` (variable is set when activating a conda environment) is used as conda prefix. 

The recipe will install the ``celery`` package from a conda channel in a conda enviroment defined by ``CONDA_PREFIX``. It deploys a `Supervisor`_ configuration for Celery in ``{{prefix}}/etc/supervisor/conf.d/celery.conf``. Supervisor can be started with ``{{prefix}}/etc/init.d/supervisord start``.

The recipe depends on ``birdhousebuilder.recipe.conda`` and ``birdhousebuilder.recipe.supervisor``.

Supported options
=================

**anaconda-home**
   Buildout option pointing to the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

Buildout options for ``celery``:

**app**
   The application instance to use for the celery worker.

**eggs**
    A list of additional eggs you want to make available to Celery. Use this to
    add additional dependencies and the module(s) containing your task definitions.

**use-celeryconfig**
   Generate and use the ``celeryconfig.py``. Set to ``false`` if Celery is configured e.a. by `pyramid_celery <https://github.com/sontek/pyramid_celery>`_. Default: ``true``.

Celery configuration options
----------------------------

The following configuration options are supported. See `Celery documentation <http://docs.celeryproject.org/en/latest/configuration.html>`_ for more details.

**broker-url**
    The url of the broker. Default: ``redis://localhost:6379/0``

**celery-result-backend**
    The url of the backend used to store task results. Default: ``redis://localhost:6379/0``

**celery-imports**
    List of modules to import when celery starts.

**celeryd-concurrency**
    The number of concurrent worker processes/threads/green threads executing tasks. Defaults to the number of available CPUs.

**loglevel**
    Logging level, choose between DEBUG, INFO, WARNING, ERROR, CRITICAL, or FATAL. Default: WARNING


Example usage
=============

The following example ``buildout.cfg`` installs Celery with Anaconda and default options:

.. code-block:: ini 

  [buildout]
  parts = celery

  anaconda-home = /home/myself/anaconda

  [celery]
  recipe = birdhousebuilder.recipe.celery
  app = mystuff_app
  eggs = mysuff

The next example shows a configuration with ``pyramid_celery`` and enabled Flower monitoring:

.. code-block:: ini 

  [buildout]
  parts = celery

  anaconda-home = /home/myself/anaconda

  [celery]
  recipe = birdhousebuilder.recipe.celery
  app = pyramid_celery.celery_app --ini default.ini
  eggs = mysuff
  use-celeryconfig = false

