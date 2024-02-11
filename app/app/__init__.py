# app/__init__.py  for Celery it is necessary to uncomment
from .celery import app as celery_app

__all__ = ('celery_app',)
