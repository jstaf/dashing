#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A helper module to retrieve data from pyslurm. Necessary because pyslurm serves
 up some really nasty data (strings are a mix of unicode and bytes, for instance)
"""

import re
import pyslurm


def pyslurm_safe(expr):
    """
    A decorator function to safely interact with the pyslurm API.
    (pyslurm returns a ValueError for *everything*).
    """
    def _wrapper(*args, **kwargs):
        try:
            return expr(*args, **kwargs)
        except ValueError:
            return {} 
    
    return _wrapper


def get_dict(data, attr):
    """
    Get all of a specific key from a dictionary of dictionaries
    """
    return {k: v[attr] for k, v in data.items()}


def get_list(data, attr):
    """
    Get all of a specific key from a dictionary of dictionaries
    """
    return [v[attr] for v in data.values()]


def convert_dict_values(dict_values):
    return list(dict_values)[0]
    

def expand_nodes(node_expr):
    """
    Expands SLURM's special node list syntax (cac[100-200] to a list of nodes 
    [cac100, cac101, cac102, ...]
    """
    matches = re.match(r'(\w+)\[(\d+)\-(\d+)\]', node_expr).groups()
    digits = len(matches[2])
    suffixes = list(map(str, range(int(matches[1]), int(matches[2]) + 1)))
    return list(map(lambda suffix: matches[0] + left_pad(suffix, digits), 
                    suffixes))
    

def left_pad(string, digits, char='0'):
    return char * (digits - len(string)) + string


@pyslurm_safe
def nodes(ids=None):
    """
    Either return all nodes or a set of nodes from SLURM.
    """
    nodes = pyslurm.node().get()
    if ids is None:
        return nodes
    else:
        nodes_dict = {}
        if not isinstance(ids, list): ids = [ids]
        for idx in ids:
            nodes_dict[idx] = nodes[idx]
        return nodes_dict


@pyslurm_safe
def jobs(ids=None):
    """
    Either return all jobs or a set of jobs from SLURM.
    """
    if ids is None:
        return pyslurm.job().get()
    else:
        job_dict = {}
        if not isinstance(ids, list): ids = [ids]
        for job in ids:
            job_dict[int(job)] = convert_dict_values(pyslurm.job().find_id(job))
        return job_dict


@pyslurm_safe    
def config():
    return pyslurm.config().get()


@pyslurm_safe
def partitions():
    return pyslurm.partition().get()


def has_backup_controller():
    """Is there a secondary slurmctld node?"""
    conf = config()
    return conf['backup_addr'] is not None or \
            conf['backup_controller'] is not None


def slurmctld_reporting():
    """
    Returns the number of controllers that are alive.
    """
    responding = 0
    # yay duck typing...
    responding += slurmctld_ping(1)
    responding += slurmctld_ping(2)
    return responding


def slurmctld_ping(which):
    """
    Returns true if the given slurmctld (1 or 2) is alive.
    """
    try:
        pyslurm.slurm_ping(which)
        return True
    except ValueError:
        return False


def remove_down(nodes):
    up = {}
    for k, v in nodes.items():
        if 'DOWN' not in v['state']:
            up[k] = v
    return up


def nodes_reporting():
    try:
        return len(remove_down(nodes()))
    except:
        return 0
    

def total_nodes():
    return len(nodes())


def total_cpus(include_down=False):
    nodelist = nodes()
    if not include_down:
        nodelist = remove_down(nodelist)
    return sum(get_list(nodelist, 'cpus'))
    

def alloc_cpus():
    return sum(get_list(nodes(), 'alloc_cpus'))


def total_jobs():
    return len(jobs())
