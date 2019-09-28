from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views as views

urlpatterns = [
    url(r'^$', views.stayunderflow, name='stayunderflow'),
    url(r'^stayunderflow/$', views.stayunderflow, name='stayunderflow'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='stay_underflow/login.html'), name='login'),
]