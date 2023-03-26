from django.contrib import admin
from .models import numCart


@admin.register(numCart)
class CartAdmin(admin.ModelAdmin):
    pass
