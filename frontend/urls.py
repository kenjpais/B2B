from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    path('join', index),
    path('info', index),
    path('create', index),
    path('join/1', index),
    path('room/<str:roomCode>', index),
    path('chat', index),
    path('audio-player', index),
    path('upload-audio', index),
]