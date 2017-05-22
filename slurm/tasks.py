from celery.decorators import periodic_task, task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

import slurm.pyslurm_api as psapi
from .models import Job, Node

log = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*')), ignore_result=True)
def update_jobs():
    jobs = psapi.jobs()
    for job in jobs.values():
        jobid = job['job_id']
        new_vals = {
            'job_state': job['job_state'],
            'user_id': job['user_id'],
            'name': job['name'],
            'submit_time': job['submit_time'],
            'start_time': job['start_time'],
            'time_limit': job['time_limit'],
            'nodes': job['nodes'],
            'cpus_per_node': job['num_cpus'],
            'mem_per_node': job['mem_per_node']}
        Job.objects.update_or_create(job_id=jobid, defaults=new_vals)
    
    # delete jobs from db that are no longer picked up by pyslurm
    Job.objects.exclude(pk__in=jobs.keys()).delete()
    # for tests
    return True


@periodic_task(run_every=(crontab(minute='*/5')), ignore_result=True)
def update_nodes():
    """
    Update node models
    """
    for node in psapi.nodes().values():
        new_vals = {
            'state': node['state'],                
            'cpus': node['cpus'],
            'alloc_cpus': node['alloc_cpus'],
            'real_mem': node['real_memory'],
            'alloc_mem': node['alloc_mem']}
        Node.objects.update_or_create(hostname=node['name'], defaults=new_vals)
    return True

