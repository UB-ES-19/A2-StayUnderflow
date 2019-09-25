from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'', views.stayunderflow, name='stayunderflow'),
    url(r'^stayunderflow/$', views.stayunderflow, name='stayunderflow'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_m, name='login'),
]