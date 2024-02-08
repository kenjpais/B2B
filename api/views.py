from django.shortcuts import render, redirect
from rest_framework import generics, status
from .serializers import (
    RoomSerializer,
    CreateRoomSerializer,
    UpdateRoomSerializer,
    UploadSongSerializer,
)
from .models import Room, Songs, AudioFile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, FileResponse
from rest_framework import permissions

# views.py
from .models import AudioFile
from .serializers import AudioFileSerializer

from .forms import UploadAudioForm
import os


class UploadAudio(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetAudio(APIView):
    def get(self, request):
        try:
            audio_file_path = (
                "D:\\music_controller\\audio_files\\DLZ_TV_On_The_Radio.mp3"
            )
            audio_file = open(audio_file_path, "rb")
            return FileResponse(audio_file, content_type="audio/mp3")
        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def get_filename(request):
    directory_path = "D:\\music_controller\\audio_files\\"  # Replace this with the path to your directory
    filename = os.listdir(directory_path)[0]
    if filename:
        return JsonResponse(filename, status=status.HTTP_200_OK)
    return JsonResponse(
        {"error": "Error with getting list of filenames"},
        status=status.HTTP_400_BAD_REQUEST,
    )

def get_filenames(request):
    directory_path = "D:\\music_controller\\audio_files\\"  # Replace this with the path to your directory
    filenames = [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]
    
    """
    i = 0 
    data = {}
    if filenames.count != 0:
        for f in filenames:
            data[i] = f
            i+=1
        print(data)
    """
    print(filenames)
    if filenames.count != 0:
        return JsonResponse(filenames, safe=False, status=status.HTTP_200_OK)
    return JsonResponse(
        {"error": "Error with getting list of filenames"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class GetName(APIView):
    def get(self, request):
        try:
            audio_file_path = "D:\\music_controller\\audio_files\\"
            file_list = os.listdir(audio_file_path)
            data = {}
            data["file"] = file_list
            # data = {"files":file_list}
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""""
class GetAudio(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
"""


class PlayAudio(generics.ListAPIView):
    def get(self, request, format=None):
        queryset = AudioFile.objects.all()
        if queryset:
            serializer_class = AudioFileSerializer
            data = AudioFileSerializer(queryset[0]).data
            return Response(data, status=status.HTTP_200_OK)
        return Response({"Error": "Cannot be found"}, status=status.HTTP_404_NOT_FOUND)


# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"Room Not Found": "Invalid Room Code."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"Bad Request": "Code paramater not found in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)

            return Response(
                {"Bad Request": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"Bad Request": "Invalid post data, did not find a code key"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                self.request.session["room_code"] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
                self.request.session["room_code"] = room.code
                return Response(
                    RoomSerializer(room).data, status=status.HTTP_201_CREATED
                )

        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {"code": self.request.session.get("room_code")}
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({"Message": "Success"}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            code = serializer.data.get("code")

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response(
                    {"msg": "Room not found."}, status=status.HTTP_404_NOT_FOUND
                )

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response(
                    {"msg": "You are not the host of this room."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response(
            {"Bad Request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST
        )


class UploadSong(APIView):
    serializer_class = UploadSongSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            room = Room.objects.filter(self.request.session.get("room_code"))
            if not room.exists():
                return Response(
                    {"msg": "Room Not Found - Cannot Upload song"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            song = Songs.objects.filter("")
            song.user = serializer.data.get("user")
            song.title = serializer.data.get("title")
            song.description = serializer.data.get("description")
            return Response(
                {"msg": "Song Uploaded Successfully"}, status=status.HTTP_201_CREATED
            )
