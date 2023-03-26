from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from . import serializers
from .models import User, Activite
import jwt
from rest_framework import status, exceptions, permissions
from django.contrib.auth import authenticate, login, logout
from lectures.models import Lecture, CalculatedLecture


# 유저 프로필 관련 view
class UserProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = User.objects.get(memberId=request.user.memberId)
        serializer = serializers.OneUserSerializer(user)
        cal_lectures = user.calculatedLecture.all()
        lecture_count = len(cal_lectures)
        is_completed_list = []
        is_completed_dict = {}
        for cal_lec in cal_lectures:
            for i in range(1, lecture_count + 1):
                try:
                    is_completed = WatchedLecture.objects.get(
                        user=user, lecture=cal_lec, lecture_num=i
                    ).is_completed
                except WatchedLecture.DoesNotExist:
                    is_completed = False
                is_completed_list.append(is_completed)

            percent = is_completed_list.count(True) / len(is_completed_list) * 100
            is_completed_list = []
            is_completed_dict.update({cal_lec.lecture.lectureTitle: percent})

        # Add is_completed_dict to serializer.data dictionary
        response_data = serializer.data.copy()
        response_data["is_completed_dict"] = is_completed_dict

        return Response(response_data)

    def put(self, request):
        user = request.user
        serializer = serializers.OneUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.OneUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 비밀번호 변경
class UserPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise exceptions.ParseError("이전 비밀번호와 새로운 비밀번호가 필요합니다.")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 유저 회원가입 관련 view
class UsersView(APIView):
    def post(self, request):
        password = request.data.get("password")
        # password 예외처리는 이곳
        if not password:
            raise exceptions.ParseError("password is required")

        serializer = serializers.OneUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.OneUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## username 유효성 판단
class UsernameView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        username = User.objects.filter(username=username)

        if username.exists():
            return Response("중복된 아이디 입니다.", status=status.HTTP_200_OK)
        else:
            return Response("사용해도 좋습니다.", status=status.HTTP_200_OK)


## 이메일 인증


# login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise exceptions.ParseError("username or password is required")

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            print(user)
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.ValidationError("username or password is incorrect")


# logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"logout": "True"})


# JWT login
class JWTokenView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise exceptions.ParseError()

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode(
                {
                    "id": user.memberId,
                    "username": user.username,
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            print(token)
            return Response({"token": token})
        else:
            return exceptions.ValidationError("username or password is incorrect")

    # 강사 update


class AddInstructor(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        all_user = User.objects.all()
        serializer = serializers.InstructorSerializer(all_user, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.InstructorSerializer(
            user,
            data=request.data,
            partial=True,
            # isInstructor =true 보내주기 요청
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.InstructorSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ActiviteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(memberId=request.user.memberId)
        serializer = serializers.ActiviteSerializer(user)
        return Response(serializer.data)


# 강의 추가 모델


class AddCalculateLecturesView(APIView):
    permission_classes = [IsAuthenticated]

    def get_calculate_lectures(self, lectureId):
        try:
            lecture = Lecture.objects.get(LectureId=lectureId)
            return CalculatedLecture.objects.get(lecture=lecture)
        except Lecture.DoesNotExist:
            raise ValueError

    def get(self, request, lectureId):
        user = request.user
        serializer = serializers.UserLedetaileSerializer(user)
        return Response(serializer.data)

    def put(self, request, lectureId):
        try:
            calculated_lecture = self.get_calculate_lectures(lectureId)
            print(calculated_lecture)
            user = request.user

            user.calculatedLecture.add(calculated_lecture)

            serializer = serializers.UserLedetaileSerializer(user)
            print(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (User.DoesNotExist, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


from watchedlectures.models import WatchedLecture


# 유저 프로필 관련 view
class UsertempProfileView(APIView):
    def get(self, request):
        user = User.objects.get(memberId=request.user.memberId)
        serializer = serializers.OneUserSerializer(user)
        cal_lectures = user.calculatedLecture.all()
        lecture_count = len(cal_lectures)
        is_completed_list = []
        is_completed_dict = {}
        for cal_lec in cal_lectures:
            for i in range(1, lecture_count + 1):
                try:
                    is_completed = WatchedLecture.objects.get(
                        user=user, lecture=cal_lec, lecture_num=i
                    ).is_completed
                except WatchedLecture.DoesNotExist:
                    is_completed = False
                is_completed_list.append(is_completed)
            percent = is_completed_list.count(True) / len(is_completed_list) * 100
            is_completed_dict.update({cal_lec.lecture.lectureTitle: percent})

        # Add is_completed_dict to serializer.data dictionary
        response_data = serializer.data.copy()
        response_data["is_completed_dict"] = is_completed_dict

        return Response(response_data)

    def put(self, request):
        user = request.user
        serializer = serializers.OneUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.OneUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
