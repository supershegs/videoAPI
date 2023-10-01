from django.urls import path
from .views import *

urlpatterns = [
    path('up/', upload_video, name='upload_video'),
    path('videos',vidoes ,name='video_list'),
    path('video/<int:pk>/', video_detail, name='video_detail'),
    # path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('upload/', VideoChunkUploadView.as_view(), name='video-chunk-upload'),
]