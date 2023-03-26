from rest_framework import serializers
from .models import Category


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    parent = ParentSerializer()

    class Meta:
        model = Category

        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]
