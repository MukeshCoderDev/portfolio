# Config package
default_app_config = 'config'

# Celery app import for Django
from .celery import app as celery_app

__all__ = ('celery_app',)
