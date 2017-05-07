from django.shortcuts import render
from django.http import HttpResponse

import slurm.pyslurm_api as psapi

def index(request):
    context = {'controllers_up': psapi.ping_controllers(),
            'nodes_reporting': psapi.nodes_reporting(),
            'total_nodes': psapi.total_nodes()}
    return render(request, 'slurm/index.html', context)

