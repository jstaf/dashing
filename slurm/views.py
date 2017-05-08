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


class NodeView(generic.ListView):
    model = Node


def nodes(request):
    update_nodes()
    return HttpResponse(Node.objects.all())


def update_nodes():
    """
    Update node models
    """
    for node in psapi.nodes().values():
        new_node = Node(
                hostname=node['name'],
                state=node['state'],
                cpus=node['cpus'],
                alloc_cpus=node['alloc_cpus'],
                real_mem=node['real_memory'],
                alloc_mem=node['alloc_mem'],
                tmp_disk=node['tmp_disk'])
        if new_node.pk not in Node.objects.all():
            new_node.save()


