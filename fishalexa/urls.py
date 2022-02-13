from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('video_stream', views.video_stream, name='video_stream'),
    path('feed', views.feed, name='feed_action'),
    path('light-on', views.light_on, name='light_on'),
    path('light-off', views.light_off, name='light_off'),
]
