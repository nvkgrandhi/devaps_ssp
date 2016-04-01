from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts_home/', views.admin_home, name='admin_home'),
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^register/', views.register, name='register'),
    url(r'^list_users/', views.list_users, name='list_users'),
    url(r'^delete_user/(?P<user_id>\d+)$', views.delete_user, name='delete_user'),
    url(r'^update/', views.update, name='update'),
    url(r'^update_user/(?P<user_id>\d+)$', views.update_user, name='update_user'),
    url(r'^user_view/', views.user_view, name='user_view'),
    url(r'^create_file/', views.create_file, name='create_file'),
    url(r'^execute_jenkins/', views.execute_jenkins, name='execute_jenkins'),
]
