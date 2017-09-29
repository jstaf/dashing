"""
Wrapper for highcharts.js
"""

import string
import random
import json

import slurm.pyslurm_api as psapi
from slurm.models import ClusterSnapshot

def random_string(length=16):
    return ''.join(random.choice(string.ascii_letters) for n in range(length))


def dump_field(queryset, field):
    return psapi.get_list(queryset.values(field), field)


def nodes_status():
    return highchart(
        'line', 
        data_series={
            'Total Nodes': dump_field(ClusterSnapshot.objects, 'nodes_total'), 
            'Nodes Alive': dump_field(ClusterSnapshot.objects, 'nodes_alive'),
            'Nodes Allocated': dump_field(ClusterSnapshot.objects, 'nodes_alloc')
        }, 
        title='Node status',
        style='height:400px;',
        class_id='col-md-6',
        div_name='test-nodes',
        xAxis={'title': {'text': 'date'}}
    )


def jobs_status():
    return highchart(
        'line', 
        data_series={
            'Jobs running': dump_field(ClusterSnapshot.objects, 'jobs_running'), 
            'Jobs pending': dump_field(ClusterSnapshot.objects, 'jobs_pending'),
            'Other jobs': dump_field(ClusterSnapshot.objects, 'jobs_other')
        }, 
        title='Job queue',
        style='height:400px;',
        class_id='col-md-6',
        div_name='test-jobs',
        xAxis={'title': {'text': 'date'}}
    )


def highchart(chart_type, data_series, title=None,
              div_name='plot-' + random_string(), 
              style='', class_id='', **kwargs):
    """
    Format data nicely for Highcharts.js
    """
    chart_data = {
        'chart': {'type': chart_type},
        'title': {'text': title, 'align': 'left'},
        'xAxis': {'title': {'text': None}},
        'yAxis': {'title': {'text': None}},
        'series': []
    }

    for name in sorted(data_series.keys()):
        chart_data['series'].append({
            'name': name,
            'data': data_series[name]
        })
    
    for k, v in kwargs.items():
        chart_data[k] = v

    html = '''
    <div id="{}" class="{}" style="{}"></div>
    <script type="text/javascript">
    $(function() {{
        var chart = Highcharts.chart('{}', {});
    }});
    </script>
    '''.format(div_name, class_id, style, div_name, json.dumps(chart_data))

    return html
