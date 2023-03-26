from django.urls import path
from . import views

urlpatterns = [
    path("<int:lectureId>/<int:num>", views.WatchedLectureView.as_view()),
]
