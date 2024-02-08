from django.urls import path
from .views import (
    RoomView,
    CreateRoomView,
    GetRoom,
    JoinRoom,
    UserInRoom,
    LeaveRoom,
    UpdateRoom,
    UploadSong,
    UploadAudio,
    GetAudio,
    GetName,
    get_filenames,
    get_filename
)  # , AudioFileAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("room", RoomView.as_view()),
    path("create-room", CreateRoomView.as_view()),
    path("get-room", GetRoom.as_view()),
    path("join-room", JoinRoom.as_view()),
    path("user-in-room", UserInRoom.as_view()),
    path("leave-room", LeaveRoom.as_view()),
    path("update-room", UpdateRoom.as_view()),
    path("upload-song", UploadSong.as_view()),
    path("upload-audio", UploadAudio.as_view(), name="upload_audio"),
    path("get-audio", GetAudio.as_view(), name="get_audio"),
    path("get-filenames/", get_filenames, name="get_filenames"),
    path("get-track-name", get_filename, name="get_filename"),
    # path('play-audio', AudioFileAPIView.as_view(), name='audio-list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
