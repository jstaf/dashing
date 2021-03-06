import math
import numpy as np

def pager(redirect_path, n_objects, page=0, page_size=50):
    """
    Create a paging object to allow paging through results.
    """
    n_pages = math.ceil(n_objects / page_size)
    if n_pages <= 1:
        # no pager needed
        return ''

    prev_page = np.clip(page - 1, 0, n_pages)
    next_page = np.clip(page + 1, 0, n_pages)

    html = '<nav aria-label="model-pager">\n'
    html += '\t<ul class="pagination">\n'
    html += '\t\t<li class="page-item"><a class="page-link" href="{}/{}">Previous</a></li>'.format(redirect_path, prev_page)
    # generate pager links
    for possible in range(np.clip(page - 2, 0, n_pages), np.clip(page + 2, 0, n_pages) + 1):
        if possible == page:
            html += '\t\t<li class="page-item active"><a class="page-link" href="{}/{}">{}</a></li>'.format(redirect_path, possible, possible + 1)
        else:
            html += '\t\t<li class="page-item"><a class="page-link" href="{}/{}">{}</a></li>'.format(redirect_path, possible, possible + 1)

    html += '\t\t<li class="page-item"><a class="page-link" href="{}/{}">Next</a></li>'.format(redirect_path, next_page)
    # close pager
    html += '\t</ul>\n</nav>\n'
    return html

