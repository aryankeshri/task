from django.conf.urls import url
from django.views.generic import TemplateView

from .views import *


urlpatterns = [
    url(r'^task/create/$', TaskView.as_view({'post': 'create_task'})),
    url(r'^api/task/dashboard/$', TaskView.as_view({'get': 'dashboard'})),
    url(r'^task/dashboard/$', TemplateView.as_view(template_name="dashboard.html")),
    url(r'^task/delete/(?P<pk>[0-9]+)/$', TaskView.as_view({'delete': 'task_delete'})),
    url(r'^task/status/change/(?P<pk>[0-9]+)/$',
        TaskView.as_view({'post': 'status_change'})),
    url(r'^task/details/(?P<pk>[0-9]+)/$',
        TaskView.as_view({'get': 'task_details'})),
    url(r'^task/update/(?P<pk>[0-9]+)/$', TaskView.as_view({'put': 'update_task'})),
    url(r'^user/data/$', UserDataView.as_view({'get': 'get'})),
]
