from django.urls import re_path, path

from . import views
from .views import post_detail

urlpatterns = [
    re_path(r'^$', views.PostListView.as_view(), name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    re_path(r'^create/$', views.post_create, name='post_create'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('reply_delete/<int:pk>/', views.reply_delete, name='reply_delete'),
    path('post_edit/<int:pk>/', views.post_edit, name='post_edit'),
]