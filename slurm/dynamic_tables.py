"""
A set of functions to generate complex HTML content as a 
single Django template variable
"""

import re
from datetime import datetime

from django.utils import timezone

def dynamic_table(queryset):
    """
    Generate a dynamic table to be served up as a single variable in template.
    """
    if len(queryset) == 0:
        return '<p>No data to display.</p>'

    model = queryset.model
    
    # table headers
    model_fields = [field.name for field in model._meta.get_fields()]
    table = '<table class="table table-striped table-hover">\n\t<thead>'
    for header in model_fields:
        table += '\t\t<th>' + str(header) + '</th>\n'
    table += '\t</thead>\n'
    
    # table contents
    model_data = queryset.values_list()
    table += '\t<tbody>\n'
    for row in model_data:
        table += '\t\t<tr>\n'
        for element in row:
            table += '\t\t\t<td>' + str(element) + '</td>\n'
        table += '\t\t</tr>\n'
    table += '\t</tbody>\n</table>'
    
    return table
    

def dynamic_table_link(queryset, redirect_path):
    """
    A dynamic table that links to a page with it's primary key
    """
    if len(queryset) == 0:
        return '<p>No data to display.</p>'

    model = queryset.model
    
    # table headers
    model_fields = []
    time_fields = []
    for idx, field in enumerate(model._meta.get_fields()):
        model_fields.append(field.name)
        if '_time' in field.name:
            time_fields.append(idx)
        if field.primary_key:
            # the index of the field that is the primary key for the model
            pk_idx = idx

    table = '<table class="table table-striped table-hover" style="cursor: pointer;">\n\t<thead>'
    for header in model_fields:
        table += '\t\t<th>' + str(header) + '</th>\n'
    table += '\t</thead>\n'
    
    # table contents
    model_data = queryset.values_list()
    table += '\t<tbody>\n'
    for row in model_data:
        table += '\t\t<tr onclick=window.document.location="%s/%s">' % (redirect_path, row[pk_idx])
        for idx, element in enumerate(row):
            if idx in time_fields:
                element = convert_time(element)
            table += '<td>%s</td>' % element
        table += '</tr>\n'
    table += '\t</tbody>\n</table>'
    
    return table
    

def dict_table(some_dict):
    table = '<table class="table table-striped">\n\t<thead>\n\t\t<th>key</th>\n\t\t<th>value</th>\n\t</thead>\n\t<tbody>'
    
    for key in sorted(some_dict.keys()):
        if key == 'batch_script' and some_dict['batch_script'] is not None:
            some_dict['batch_script'] = re.sub(r'\n', '<br>', some_dict['batch_script'])
        elif 'time' in key and some_dict[key] is not None:
            if ':' not in str(some_dict[key]) and float(some_dict[key]) > 1000000:
                some_dict[key] = convert_time(some_dict[key])
        table += '<tr><td>%s</td><td>%s</td></tr>' % (key, some_dict[key])

    table += '\n\t</tbody>\n</table>'
    return table


def convert_time(timestamp):
    if isinstance(timestamp, datetime):
        time = timestamp
    else:
        time = datetime.fromtimestamp(float(timestamp), timezone.get_current_timezone())
    return time.strftime('%Y-%m-%d %H:%M:%S %Z')

