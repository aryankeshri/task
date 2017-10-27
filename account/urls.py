from django.conf.urls import url
from django.views.generic import TemplateView

from .views import *


urlpatterns = [
    url(r'^api/signup/$', SignUpView.as_view({'post': 'register'})),
    url(r'^signup/$', TemplateView.as_view(template_name="signup.html")),
    url(r'^api/login/$', Login.as_view({'post': 'post'})),
    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^change/password/$', ChangePasswordView.as_view({'post': 'post'})),
    url(r'^forget/password/$', ResetPasswordView.as_view({'post': 'reset'})),
    url(r'^forget/password/done/$', ResetPasswordView.as_view({'post': 'reset_done'})),
    url(r'^logout/$', Logout.as_view()),
    url(r'^test/$', html_test),
    ]