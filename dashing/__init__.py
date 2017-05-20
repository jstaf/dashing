from __future__ import absolute_import

# force celery to load on django start
from .celery import app as celery_app
