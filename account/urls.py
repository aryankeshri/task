from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view({'post': 'register'}))
    ]