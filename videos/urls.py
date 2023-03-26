from django.urls import path
from . import views

urlpatterns = [
    path("", views.VideoList.as_view()),
    path("lectures/<int:lectureId>", views.LectureVideoList.as_view()),
    path("<int:pk>", views.oneVideo.as_view()),
    path("lectures/<int:lectureId>/upload", views.UploadVideoView.as_view()),
    path("lectures/<int:lectureId>/<int:num>", views.VideosLists.as_view()),
]
