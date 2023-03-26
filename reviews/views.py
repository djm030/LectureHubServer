from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review, Reply
from users.models import User
from .serializers import (
    ReviewSerializer,
    ReviewMakeSerializer,
    ReplySerializer,
    ReplymakeSerializer,
    ReviewmainpageSerializer,
)
from rest_framework.exceptions import ParseError, NotFound
from lectures.models import Lecture


class UserNameReview(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)

            user_review = Review.objects.filter(author=user)
        except Review.DoesNotExist:
            raise NotFound
        serializer = ReviewSerializer(user_review, many=True)
        return Response(serializer.data)


class ReviewView(APIView):
    def get(self, request, lectureId):
        lecture = Lecture.objects.get(LectureId=lectureId)
        all_review = Review.objects.filter(lecture=lecture, rating__gte=4)
        serializer = ReviewmainpageSerializer(all_review, many=True)
        return Response(serializer.data)

    def post(self, request, lectureId):
        lecture = Lecture.objects.get(LectureId=lectureId)
        user = request.user

        serializer = ReviewMakeSerializer(
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            review = serializer.save(lecture=lecture, user=user)
            serializer = ReviewMakeSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ReplyView(APIView):
    def get(self, request, lectureId, reviewId):
        all_reply = Reply.objects.filter(review=reviewId)
        serializer = ReplySerializer(all_reply, many=True)
        return Response(serializer.data)

    def post(self, request, lectureId, reviewId):
        user = request.user
        review = Review.objects.get(id=reviewId)
        serializer = ReplymakeSerializer(
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            reply = serializer.save(
                user=user,
                review=review,
            )
            serializer = ReplySerializer(reply)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
