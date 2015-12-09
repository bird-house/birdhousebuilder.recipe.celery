###
# celery scheduler config
# http://celery.readthedocs.org/en/latest/configuration.html
###

## Broker settings.
BROKER_URL = 'redis://localhost:6379/0'

## Backend to store task state and results.
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('myapp.tasks', )
