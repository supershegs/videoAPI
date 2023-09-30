from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoForm
from .models import *
from .serializers import *


import os

import speech_recognition as sr
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
# video_app/views.py



def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')  # Redirect to a video list page
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

def vidoes(request):
    videolist = Video.objects.all()
    for video in videolist:
        print(video.manuscript)
    return render(request, 'video.html', {'videolist': videolist})


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'video_detail.html', {'video': video})


class VideoUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        video_file = request.data.get('video_file')
        # C:\Users\oluwasegun.tinuala\Documents\class\chek.mp4
    
        # video_file = r'C:\Users\oluwasegun.tinuala\Documents\class\chek.mp4'
        


        if not video_file:
            return Response({'error': 'No video file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the video file
        video = Video.objects.create(video_file=video_file)

        # Perform automatic speech recognition (ASR) to generate manuscript
        recognizer = sr.Recognizer()
        video_path = os.path.join('media', str(video.video_file))
        with sr.AudioFile(video_path) as source:
            audio_data = recognizer.record(source)
            manuscript = recognizer.recognize_google(audio_data)

        video.manuscript = manuscript
        video.save()

        serializer = VideoSerializer(video)
        print()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
