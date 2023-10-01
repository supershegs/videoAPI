# your_app/serializers.py

from rest_framework import serializers
from .models import Video
from .models import VideoChunk

class VideoChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChunk
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
