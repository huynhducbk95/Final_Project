

from django.urls import path

from . import views


urlpatterns = [
    path(r'show_database/', views.show_database, name='show_database'),
    path(r'query/', views.query, name='query'),
]