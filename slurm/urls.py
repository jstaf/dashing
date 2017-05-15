from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodes/?$', views.nodes, name='nodes'),
    url(r'^nodes/(?P<node_id>\w+)/?$', views.node_page, name='node_page'),
    url(r'^jobs/?$', views.jobs, name='jobs'),
    url(r'^jobs/(?P<job_id>\d+)/?$', views.job_page, name='job_page'),
]

