from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodes/(?P<page>\d+)?/?$', views.nodes, name='nodes'),
    url(r'^nodes/id/(?P<node_id>\w+)/?$', views.node_page, name='node_page'),
    url(r'^jobs/(?P<page>\d+)?/?$', views.jobs, name='jobs'),
    url(r'^jobs/id/(?P<job_id>\d+)/?$', views.job_page, name='job_page'),
    url(r'^search/(?P<search_str>.*)/?$', views.search, name='search'),
]
