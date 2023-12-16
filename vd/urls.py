from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dub/', views.dub, name='dub'),
    path('play_dubbed_video/', views.play_dubbed_video, name='play_dubbed_video'),

]