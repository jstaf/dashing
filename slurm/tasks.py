"""
Various functions to be run periodically by celery (like cron).
"""

import time
import datetime

from celery.decorators import periodic_task, task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.utils import timezone
import redis

import slurm.pyslurm_api as psapi
from .models import Job, Node, ClusterSnapshot

log = get_task_logger(__name__)

class RedisLock():
    """Because the redlock algorithm sucks"""

    def __init__(self, name):
        self.name = name
        self.instance = redis.Redis()


    def __enter__(self):
        self.acquire()
    

    def __exit__(self, type_, value, traceback):
        self.release()


    def acquire(self):
        while not self.instance.setnx(self.name, 'lock'):
            time.sleep(0.1)

    
    def release(self):
        self.instance.delete(self.name)
        

@periodic_task(run_every=(crontab(minute='*')), ignore_result=True)
def update_jobs():
    jobs = psapi.jobs()
    tz = timezone.get_current_timezone()
    with RedisLock('db'):
        for job in jobs.values():
            jobid = job['job_id']
            new_vals = {
                'job_state': job['job_state'],
                'user_id': job['user_id'],
                'name': job['name'],
                'submit_time': datetime.datetime.fromtimestamp(job['submit_time'], tz),
                'start_time': datetime.datetime.fromtimestamp(job['start_time'], tz),
                'time_limit': job['time_limit'],
                'nodes': job['nodes'],
                'cpus_per_node': job['num_cpus'],
                'mem_per_node': job['mem_per_node']}
            Job.objects.update_or_create(job_id=jobid, defaults=new_vals)
            # delete jobs from db that are no longer picked up by pyslurm
            Job.objects.exclude(pk__in=jobs.keys()).delete()
    return True


@periodic_task(run_every=(crontab(minute='*/5')), ignore_result=True)
def update_nodes():
    """
    Update node models
    """
    with RedisLock('db'):
        for node in psapi.nodes().values():
            new_vals = {
                'state': node['state'],                
                'cpus': node['cpus'],
                'alloc_cpus': node['alloc_cpus'],
                'real_mem': node['real_memory'],
                'alloc_mem': node['alloc_mem']}
            Node.objects.update_or_create(hostname=node['name'], defaults=new_vals)
    return True


def cluster_snapshot():
    """Grab periodic stats about cluster"""
    with RedisLock('db'):
        snapshot = ClusterSnapshot()
    return True

