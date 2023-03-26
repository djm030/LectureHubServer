from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import numCart
from users.models import User
from . import serializers
from rest_framework import permissions


class CartView(APIView):
    def get(self, request):
        all_numCart = numCart.objects.all()
        serializer = serializers.CartSerializer(all_numCart, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.ActivitCartSerializereSerializer(
            user,
            data=request.data,
            partial=True,
            # isInstructor =true 보내주기 요청
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.CartSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
