#!/bin/bash

redis-server &

rm -f celerybeat.pid
celery -A dashing worker -l info &
celery -A dashing beat -l info & 
sleep 5 
python3 manage.py runserver 0.0.0.0:8000
