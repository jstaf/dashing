from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
import numpy as np

from .models import Node, Job, ClusterSnapshot
import slurm.ui.dynamic_tables as dt
import slurm.ui.pager as pager
import slurm.ui.plots as plots
import slurm.pyslurm_api as psapi

page_size = 50

def index(request):
    cs = ClusterSnapshot.objects.latest('time')
    context = {
        'status': {
            'slurmctld_up': cs.slurmctld_alive > 0,
            'avg_qtime': cs.jobs_avg_qtime,
            'jobs_total': cs.jobs_running + cs.jobs_pending + cs.jobs_other,
            'cluster_load': '{}/{} ({:.1f}%)'.format(
                cs.cpus_alloc,
                cs.cpus_total, 
                cs.cpus_alloc / cs.cpus_total * 100)
        },
        'nodes': plots.nodes_status(),
        'jobs': plots.jobs_status()
    }
    return render(request, 'slurm/index.html', context)


def nodes(request, page):
    if page is None:
        page = 0
    
    page = int(page)
    start = page_size * page
    pagination = pager.pager('/slurm/nodes', Node.objects.count(), page, page_size)
    table = dt.dynamic_table_link(Node.objects.order_by('pk')[start:(start + page_size)], '/slurm/nodes')
    return render(request, 'slurm/data-table.html',
            {'page_name': 'Node status', 'dynamic_table': table, 'pager': pagination})


def jobs(request, page):
    if page is None:
        page = 0

    page = int(page)    
    start = page_size * page
    pagination = pager.pager('/slurm/jobs', Job.objects.count(), page, page_size) 
    table = dt.dynamic_table_link(Job.objects.order_by('pk')[start:(start + page_size)], '/slurm/jobs')
    return render(request, 'slurm/data-table.html', 
            {'page_name': 'Job queue', 'dynamic_table': table, 'pager': pagination})


def node_page(request, node_id):
    deets = psapi.nodes(ids=node_id)
    if len(deets) == 1:
        table = dt.dict_table(deets[node_id])
        return render(request, 'slurm/data-table.html',
                {'page_name': 'Details for node {}'.format(node_id), 'dynamic_table': table})
    else:
        raise Http404("The specified node does not exist.")


def job_page(request, job_id):
    job_id = int(job_id)
    deets = psapi.jobs(ids=job_id)
    if len(deets) == 1:
        table = dt.dict_table(deets[job_id])
        return render(request, 'slurm/data-table.html',
                {'page_name': 'Details for job {}'.format(job_id), 'dynamic_table': table})
    else:
        raise Http404("The specified job does not exist (it also may have completed).")


def search(request, search_str):
    # check if search string matches either a node name or job id. 
    # if so, just redirect to that page
    try:
        jobid = int(search_str)
        can_coerce = True
    except ValueError:
        can_coerce = False

    if search_str in [x[0] for x in Node.objects.values_list('hostname')]:
        return redirect('/slurm/nodes/id/{}'.format(search_str))
    elif can_coerce and jobid in [x[0] for x in Job.objects.values_list('job_id')]:
        return redirect('/slurm/jobs/id/{}'.format(search_str))

    # check if search string matches a set of nodes or jobs,
    # if so, display that queryset.    

    return render(request, 'slurm/search-fail.html', {'search_str': search_str})
