#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A helper module to retrieve data from pyslurm. Necessary because pyslurm serves
 up some really nasty data (strings are a mix of unicode and bytes, for instance)
"""

import re
import pyslurm


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


def to_unicode(bytes_dict):
    """
    Recursively convert a dictionary to unicode
    """
    # convert bytes to unicode
    if isinstance(bytes_dict, bytes):
        return bytes_dict.decode()
    # some strings look like unicode, but are garbled strings that need to be fixed
    elif isinstance(bytes_dict, str) and "b'" in bytes_dict:
        return re.match(r"b'(\w+)'", bytes_dict).groups()[0]
    # if a dictionary, recursively call function
    elif isinstance(bytes_dict, dict):
        return {to_unicode(k): to_unicode(v) for k, v in bytes_dict.items()}
    # otherwise leave intact
    else:
        return bytes_dict
    

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


def pyslurm_get(expr):
    """
    A wrapper function to safely handle pyslurm calls in event of controller failure
    """
    try:
        return(to_unicode(expr))
    except:
        return {} 


def nodes():
    return pyslurm_get(pyslurm.node().get())


def jobs(ids=None):
    """
    Either return all jobs or a set of jobs from SLURM.
    """
    if ids is None:
        return pyslurm_get(pyslurm.job().get())
    else:
        job_dict = {}
        if not isinstance(ids, list): ids = [ids]
        for job in ids:
            try:
                byteid = str(job).encode()
                job_dict[int(job)] = pyslurm_get(convert_dict_values(pyslurm.job().find_id(byteid)))
            except ValueError as e:
                pass   # job not found, no need to throw a fucking exception
        return job_dict

    
def config():
    return pyslurm_get(pyslurm.config().get())


def partitions():
    return pyslurm_get(pyslurm.partition().get())


def has_backup_controller():
    """Is there a secondary slurmctld node?"""
    config = config()
    return config['backup_addr'] is not None or \
            config['backup_controller'] is not None

    
def ping_controllers():
    """Returns True if any slurmctld is alive"""

    # why can't this function just return false if it fails???
    try:
        pyslurm.slurm_ping(1)
        return True
    except:
        try:
            pyslurm.slurm_ping(2)
            return True
        except:
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


def total_cpus(include_down = False):
    nodes = nodes()
    if not include_down:
        nodes = remove_down(nodes)
    return sum(get_list(nodes, 'cpus'))
    

def alloc_cpus():
    return sum(get_list(nodes(), 'alloc_cpus'))


def total_jobs():
    return len(jobs())


