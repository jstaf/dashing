from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Node, Job
import slurm.dynamic_tables as dt
import slurm.pyslurm_api as psapi

def index(request):
    context = {'controllers_up': psapi.ping_controllers(),
            'nodes_reporting': psapi.nodes_reporting(),
            'total_nodes': psapi.total_nodes()}
    return render(request, 'slurm/index.html', context)


def nodes(request):
    update_nodes()
    table = dt.dynamic_table_link(Node.objects.order_by('pk'), '/slurm/nodes')

    return render(request, 'slurm/data-table.html',
            {'page_name': 'Node status', 'dynamic_table': table})


def jobs(request):
    update_jobs()
    table = dt.dynamic_table_link(Job.objects.order_by('pk'), '/slurm/jobs')
    
    return render(request, 'slurm/data-table.html', 
            {'page_name': 'Job queue', 'dynamic_table': table})


def node_page(request, node_id):
    deets = psapi.nodes(ids = node_id)
    if len(deets) == 1:
        table = dt.dict_table(deets[node_id])
        return render(request, 'slurm/data-table.html',
                {'page_name': 'Details for node {}'.format(node_id), 'dynamic_table': table})
    else:
        raise Http404("The specified node does not exist.")


def job_page(request, job_id):
    job_id = int(job_id)
    deets = psapi.jobs(ids = job_id)
    if len(deets) == 1:
        table = dt.dict_table(deets[job_id])
        return render(request, 'slurm/data-table.html',
                {'page_name': 'Details for job {}'.format(job_id), 'dynamic_table': table})
    else:
        raise Http404("The specified job does not exist (it also may have completed).")


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
        new_node, created = Node.objects.update_or_create(
                hostname=node['name'], defaults=new_vals)

