from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Node, Job
import slurm.pyslurm_api as psapi

def index(request):
    context = {'controllers_up': psapi.ping_controllers(),
            'nodes_reporting': psapi.nodes_reporting(),
            'total_nodes': psapi.total_nodes()}
    return render(request, 'slurm/index.html', context)


def nodes(request):
    update_nodes()
    fields = [field.name for field in Node._meta.get_fields()]
    
    # collapse everything to a really long list for use in django template (also, fuck me)
    nodes = Node.objects.order_by('pk').values_list()
    node_data = []
    for node in nodes:
        node_data.append('!tr_start')
        node_data.extend(list(node))
        node_data.append('!tr_stop')

    return render(request, 'slurm/node_list.html',
            {'fields': fields, 'num_fields': str(len(fields)), 'node_data': node_data })


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

