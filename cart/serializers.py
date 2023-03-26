from rest_framework import serializers
from .models import numCart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = numCart
        fields = "__all__"
