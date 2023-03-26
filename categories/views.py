from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework.exceptions import NotFound


class Categories(APIView):
    def get(self, request):
        classification = Category.objects.all()
        serializer = CategorySerializer(classification, many=True)
        return Response(serializer.data)


class oneCategory(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(
                CategorySerializer(updated_category).data,
            )
        else:
            return Response(serializer.errors)
