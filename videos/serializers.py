from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Video
from lectures.serializers import LectureTitleSerializer

# from lectures.serializers import LectureTitleSerializer


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VideoListSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "title",
            "description",
            "videoLength",
        )


class VideoDetailSerializer(ModelSerializer):
    calculatedLecture = LectureTitleSerializer()

    class Meta:
        model = Video
        fields = ("videoFile", "calculatedLecture")
