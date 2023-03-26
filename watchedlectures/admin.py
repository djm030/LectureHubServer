from django.contrib import admin
from .models import WatchedLecture


@admin.register(WatchedLecture)
class WatchedLectureAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lecture",
    ]
    list_filter = [
        "user",
        "lecture",
    ]
    search_fields = [
        "user",
        "lecture",
    ]
