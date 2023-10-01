from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoForm
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


import os

import speech_recognition as sr
from rest_framework import status
from rest_framework.parsers import FileUploadParser






# api/views.py
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from django.conf import settings
import moviepy.editor as mp


from rest_framework.parsers import FileUploadParser

from .models import VideoChunk
from .serializers import VideoChunkSerializer

class VideoChunkUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, format=None):
        serializer = VideoChunkSerializer(data=request.data)
        if serializer.is_valid():
            # Save the video chunk to the 'media/chunks/' directory
            video_chunk_instance = serializer.save()

            # Convert video chunk to audio
            video_path = video_chunk_instance.video_chunk.path
            audio_path = os.path.splitext(video_path)[0] + ".mp3"
            video_clip = mp.VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path)

            # Transcribe audio to manuscript
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                manuscript = recognizer.recognize_google(audio)

            # Update the video chunk instance with the manuscript
            video_chunk_instance.manuscript = manuscript
            video_chunk_instance.save()

            return Response(VideoChunkSerializer(video_chunk_instance).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class VideoUpView(APIView):
    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Get the uploaded video file
            video_instance = serializer.instance
            video_path = video_instance.video_file.path

            # Convert video to audio
            audio_path = os.path.splitext(video_path)[0] + ".mp3"
            video_clip = mp.VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path)

            # Transcribe audio to manuscript
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                manuscript = recognizer.recognize_google(audio)

            # Update the video instance with the manuscript
            video_instance.manuscript = manuscript
            video_instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


# class VideoUploadView(APIView):
    # parser_class = (FileUploadParser,)

    # def post(self, request, *args, **kwargs):
    #     video_file = request.data.get('video_file')
    #     # C:\Users\oluwasegun.tinuala\Documents\class\chek.mp4
    
    #     # video_file = r'C:\Users\oluwasegun.tinuala\Documents\class\chek.mp4'
        


    #     if not video_file:
    #         return Response({'error': 'No video file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Save the video file
    #     video = Video.objects.create(video_file=video_file)

    #     # Perform automatic speech recognition (ASR) to generate manuscript
    #     recognizer = sr.Recognizer()
    #     video_path = os.path.join('media', str(video.video_file))
    #     with sr.AudioFile(video_path) as source:
    #         audio_data = recognizer.record(source)
    #         manuscript = recognizer.recognize_google(audio_data)

    #     video.manuscript = manuscript
    #     video.save()

    #     serializer = VideoSerializer(video)
    #     print()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
