from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodes$', views.nodes, name='nodes'),
    url(r'^jobs$', views.jobs, name='jobs'),
]

