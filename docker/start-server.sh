#!/bin/bash

redis-server &
/usr/bin/python3 /root/dashing/manage.py runserver 0.0.0.0:8000

