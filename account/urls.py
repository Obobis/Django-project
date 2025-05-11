from tempfile import template

from django.urls import re_path, path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.contrib.auth import views as auth_views

from .views import EmailConfirm

app_name = 'account'

urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    re_path(r'^logout-then-login/$', views.user_logout, name='logout_then_login'),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^password-change/$', views.change_password, name='password_change'),
    re_path(r'^password-change/done/$', views.password_change_done, name='password_change_done'),
    re_path(r'^password-reset/$',
            views.UserChangePassword,
            name='_password_reset'),
    re_path(r'^password-reset/done/$',
            views.PasswordResetForm,
            name='password_reset_done'),
    re_path(r'^password-reset/confirm/',
            EmailConfirm.as_view(),
            name='password_reset_confirm'),
    re_path(r'^password-reset/complete/$',
            auth_views.PasswordResetCompleteView.as_view(),
            name='password_reset_complete'),
    re_path(r'^registration/$', views.register, name='register'),
    re_path(r'^edit/$', views.edit, name='edit'),
]
