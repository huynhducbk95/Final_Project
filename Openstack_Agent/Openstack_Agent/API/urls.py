from django.urls import path

from . import views


urlpatterns = [
    path(r'workload_list/', views.workload_list, name='workload_list'),
    path(r'check_ping/', views.check_ping, name='check_ping'),
    path(r'check_workload_ping/', views.check_workload_ping, name='check_workload_ping'),
    path(r'add_nic/', views.add_nic, name='add_nic'),
]