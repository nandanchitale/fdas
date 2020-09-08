from django.urls import path
from django.conf.urls import url

from attendance_system.views import *

urlpatterns = [
    path('', home, name = 'home'),
    #path('registerStudent', views.registerStudent, name = 'registerStudent'),
    path('registerStudent', registerStudent , name = 'registerStudent'),
    path('login', loginPage, name='login'),
    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('videoFeed/', views.getVideo, name='videoFeed'),
]