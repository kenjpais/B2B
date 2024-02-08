from django import forms
from .models import AudioFile

class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ('name', 'audio_file')