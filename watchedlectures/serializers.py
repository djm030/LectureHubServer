from rest_framework import serializers
from .models import WatchedLecture


class WatchedLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedLecture
        fields = "__all__"
