from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view({'post': 'register'})),
    url(r'^login/$', Login.as_view({'post': 'post'})),
    url(r'^change/password/$', ChangePasswordView.as_view({'post': 'post'})),
    url(r'^forget/password/$', ResetPasswordView.as_view({'post': 'reset'})),
    url(r'^forget/password/done/$', ResetPasswordView.as_view({'post': 'reset_done'})),
    url(r'^logout/$', Logout.as_view()),
    url(r'^test/$', html_test),
    ]