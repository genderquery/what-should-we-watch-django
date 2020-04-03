from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('party', views.party, name='party'),
    path('join', views.join, name='join'),
    path('start', views.start, name='start'),
    path('search', views.search, name='search'),
    path('add', views.add, name='add'),
    path('vote', views.vote, name='vote'),
]
