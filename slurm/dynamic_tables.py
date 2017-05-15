"""
A set of functions to generate complex HTML content as a 
single Django template variable
"""


def dynamic_table(queryset):
    """
    Generate a dynamic table to be served up as a single variable in template.
    """

    model = queryset.model
    
    # table headers
    model_fields = [field.name for field in model._meta.get_fields()]
    table = '<table class="table table-hover">\n\t<thead>'
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
    model = queryset.model
    
    # table headers
    model_fields = []
    for idx, field in enumerate(model._meta.get_fields()):
        model_fields.append(field.name)
        if field.primary_key:
            # the index of the field that is the primary key for the model
            pk_idx = idx

    table = '<table class="table table-hover">\n\t<thead>'
    for header in model_fields:
        table += '\t\t<th>' + str(header) + '</th>\n'
    table += '\t</thead>\n'
    
    # table contents
    model_data = queryset.values_list()
    table += '\t<tbody>\n'
    for row in model_data:
        table += '\t\t<tr onclick=window.document.location="%s/%s">' % (redirect_path, row[pk_idx])
        for element in row:
            table += '<td>%s</td>' % element
        table += '</tr>\n'
    table += '\t</tbody>\n</table>'
    
    return table
    

def dict_table(some_dict):
    table = '<table class="table">\n\t<thead>\n\t\t<th>key</th>\n\t\t<th>value</th>\n\t</thead>\n\t<tbody>'
    
    for key in sorted(some_dict.keys()):
        table += '<tr><td>%s</td><td>%s</td></tr>' % (key, some_dict[key])

    table += '\n\t</tbody>\n</table>'
    return table


