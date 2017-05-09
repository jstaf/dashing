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
    

