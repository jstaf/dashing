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
    table = dt.dynamic_table_link(Node.objects.order_by('pk'), '/slurm/nodes')
    return render(request, 'slurm/data-table.html',
            {'page_name': 'Node status', 'dynamic_table': table})


def jobs(request):
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
