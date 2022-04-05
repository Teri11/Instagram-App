from django.conf.urls import url
from django.urls import re_path,path
from django.contrib.auth import views as auth_views
from . import views as app_views

urlpatterns = [
  path('accounts/register/',app_views.register,name='register'),
  path('details/<int:post_id>',app_views.post_details,  name='post.detail'),
  path('',auth_views.LoginView.as_view(template_name = 'registration/login.html'),name='login'),
  path('add_post/',app_views.add_post,name='add_post'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html'),name='logout'),
  path('accounts/profile/',app_views.profile,name='profile'),
  path('update_user/',app_views.update_profile,name='update_user'),
  re_path(r'^user_page/(?P<pk>\d+)$',app_views.posts_profile,name='posts_profile'),
  re_path(r'^comment/(?P<post_id>\d+)$',app_views.comment,name='comment'),
  re_path(r'^like/(?P<post_id>\d+)', app_views.likes, name='likes'),
  re_path(r'^search/$',app_views.search_users,name='search'),
  re_path(r'^delete/(?P<post_id>\d+)$',app_views.delete,name='delete'),


]

