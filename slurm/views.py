from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Node, Job
from .dynamic_tables import dynamic_table, dynamic_table_link
import slurm.pyslurm_api as psapi

def index(request):
    context = {'controllers_up': psapi.ping_controllers(),
            'nodes_reporting': psapi.nodes_reporting(),
            'total_nodes': psapi.total_nodes()}
    return render(request, 'slurm/index.html', context)


def nodes(request):
    update_nodes()
    table = dynamic_table(Node.objects.order_by('pk'))

    return render(request, 'slurm/data-table.html',
            {'page_name': 'Node status', 'dynamic_table': table})


def jobs(request):
    update_jobs()
    table = dynamic_table_link(Job.objects.order_by('pk'), '/slurm/jobs')
    
    return render(request, 'slurm/data-table.html', 
            {'page_name': 'Job queue', 'dynamic_table': table})


def job_page(request, job_id):
    try:
        deets = psapi.job_id(job_id)
        return HttpResponse(deets)
    except ValueError as e:
        raise Http404("The specified job does not exist (it also may have completed).")


def update_jobs():
    jobs = psapi.jobs()
    for job in jobs.values():
        jobid = job['job_id']
        new_vals = {
            'job_state': job['job_state'],
            'user_id': job['user_id'],
            'name': job['name'],
            'command': job['command'],
            'submit_time': job['submit_time'],
            'start_time': job['start_time'],
            'time_limit': job['time_limit'],
            'nodes': job['nodes'],
            'cpus_per_node': job['num_cpus'],
            'mem_per_node': job['mem_per_node']}
        Job.objects.update_or_create(job_id=jobid, defaults=new_vals)
    
    # delete jobs from db that are no longer picked up by pyslurm
    Job.objects.exclude(pk__in=jobs.keys()).delete()


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
            'alloc_mem': node['alloc_mem'],
            'tmp_disk': node['tmp_disk']}
        new_node, created = Node.objects.update_or_create(
                hostname=node['name'], defaults=new_vals)

