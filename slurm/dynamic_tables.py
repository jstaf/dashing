"""
Generate a dynamic table to be served up as a single variable in template.
"""

def dynamic_table(queryset):
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
        pk_id = str(row[pk_idx])
        table += '\t\t<tr onclick=window.document.location="%s/%s">' % (redirect_path, pk_id)
        for element in row:
            table += '<td>%s</td>' % element
        table += '</tr>\n'
    table += '\t</tbody>\n</table>'
    
    return table
    

