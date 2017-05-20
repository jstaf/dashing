#!/bin/bash

redis-server &
celery -A dashing worker -l info &
celery -A dashing beat -l info & 
python3 manage.py runserver 0.0.0.0:8000
