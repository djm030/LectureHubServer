from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers
from watchedlectures.serializers import WatchedLectureSerializer


# 프로필 관련 serializer
class OneUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
            "last_login",
            "is_superuser",
            "loginDate",
            "lectureDate",
            "paymentDate",
            "isWithdrawn",
            "created_at",
            "Withdrawn_at",
        ]
        depth = 3


# 로그인 관련 serializer
class UserSignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "nickname",
            "phoneNumber",
            "dateBirth",
            "gender",
        )


# 강사 관련


class InstructorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "instructorField",
            "instructorAbout",
            "instructorCareer",
        )


# ACTIVITE 관련


class ActiviteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "ledetaile",
            "loginDate",
            "lectureDate",
            "paymentDate",
            "isWithdrawn",
            "created_at",
            "Withdrawn_at",
        )


class UserNameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserLedetaileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "calculatedLecture",
        )
