from django.db import models
import string
import random

def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio_files/')

class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)

class Songs(models.Model):
    user = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=8, default="unknown", unique=True)
    artist = models.TextField(max_length=240, default="unknown")
    source_type = models.CharField(max_length=10, default="unknown")
    source_path = models.TextField(max_length=500, default="unknown")

class Playlist(models.Model):
    user = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=8, default="unknown", unique=True)
    name = models.CharField(max_length=8, default="unknown", unique=True)
    songs = models.ManyToManyField(Songs)
    description = models.TextField(max_length=500, default="unknown", unique=True)

