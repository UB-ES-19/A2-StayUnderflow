from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostDetailView, Stayunderflow

from . import views as views

urlpatterns = [
    url(r'^$', Stayunderflow.as_view(), name='stayunderflow'),
    url(r'^stayunderflow/$', Stayunderflow.as_view(), name='stayunderflow'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='stay_underflow/login.html'), name='login'),
    path('stayunderflow/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # pk serà un enter que contindrà el id del post clicat
    url(r'^auth/', include('social_django.urls', namespace='social')),
]