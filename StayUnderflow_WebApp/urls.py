from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostDetailView, Stayunderflow, CreatePost, CreateAnswer

from . import views as views

urlpatterns = [
    url(r'^$', views.home, name='stayunderflow_home'),
    url(r'^stayunderflow/$', Stayunderflow.as_view(), name='stayunderflow'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='stay_underflow/login.html'), name='login'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^profile/$', views.my_profile, name='profile'),
    url(r'^profile/(?P<username>.*)/$', views.other_profile, name='profile'),
    url(r'^users/$', views.search_users, name='users'),
    path('stayunderflow/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # pk serà un enter que contindrà el id del post clicat
    path('stayunderflow/post/<int:pk>/answer/<int:id>/like', views.like_post, name='post-like'),
    path('stayunderflow/post/new/', CreatePost.as_view(), name='new-post'),
    path('stayunderflow/post/<int:pk>/answer/', CreateAnswer.as_view(), name='new-answer'),
    path('stayunderflow/post/edit/', views.update_my_profile, name='edit_profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='stay_underflow/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='stay_underflow/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='stay_underflow/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='stay_underflow/password_reset_complete.html'), name='password_reset_complete'),
]