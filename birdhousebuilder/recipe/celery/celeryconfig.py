###
# celery scheduler config
# http://celery.readthedocs.org/en/latest/configuration.html
###
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
