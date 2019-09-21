from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_m, name='login'),
    url(r'^test_login/$', views.test_login, name='test_login'),
]