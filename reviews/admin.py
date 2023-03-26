from django.contrib import admin
from .models import Review, Reply


@admin.register(Review)
class Reviewadmin(admin.ModelAdmin):
    pass


@admin.register(Reply)
class Replyadmin(admin.ModelAdmin):
    pass
