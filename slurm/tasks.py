"""
Various functions to be run periodically by celery (like cron).
"""

import time
from datetime import datetime, timedelta

from celery.task import periodic_task, task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.utils import timezone
import redis
import numpy as np

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
    # delete all jobs from db that are no longer picked up by pyslurm
    Job.objects.exclude(pk__in=jobs.keys()).delete()
    tz = timezone.get_current_timezone()
    with RedisLock('db'):
        for job in jobs.values():
            jobid = job['job_id']
            new_vals = {
                'job_state': job['job_state'],
                'user_id': job['user_id'],
                'name': job['name'],
                'submit_time': datetime.fromtimestamp(job['submit_time'], tz),
                'start_time': datetime.fromtimestamp(job['start_time'], tz),
                'time_limit': job['time_limit'],
                'nodes': job['nodes'],
                'cpus_per_node': job['num_cpus'],
                'mem_per_node': job['mem_per_node']}
            Job.objects.update_or_create(job_id=jobid, defaults=new_vals)
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


@periodic_task(run_every=(crontab(minute='*/5')), ignore_result=True)
def cluster_snapshot():
    """Grab periodic stats about cluster"""

    # db queries that would otherwise get reused
    nodes_up = Node.objects.exclude(state__in=['DOWN', 'UNKNOWN', 'NO_RESPOND', 'POWER_DOWN', 'POWER_UP'])
    jobs_running = Job.objects.filter(job_state='RUNNING')
    
    if len(jobs_running) > 0:
        # numpy complains about taking the mean of 0 items otherwise
        qtime = np.mean([queue_time(job) for job in jobs_running])
    else:
        qtime = timedelta()

    snapshot = ClusterSnapshot(
        slurmctld_alive=psapi.slurmctld_reporting(),
        nodes_total=len(Node.objects.all()),
        nodes_alive=len(nodes_up),
        nodes_alloc=len(Node.objects.filter(state__in=['ALLOC', 'MIXED'])),
        jobs_running=len(jobs_running),
        jobs_pending=len(Job.objects.filter(job_state='PENDING')),
        jobs_other=len(Job.objects.exclude(job_state__in=['RUNNING', 'PENDING'])),
        jobs_avg_qtime=qtime,
        cpus_total=np.sum(nodes_up.values_list('cpus')),
        cpus_alloc=np.sum(nodes_up.values_list('alloc_cpus'))
    )
    with RedisLock('db'):
        snapshot.save()
    return True


def queue_time(job):
    return job.start_time - job.submit_time
