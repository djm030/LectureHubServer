from django.urls import path
from . import views

urlpatterns = [
    # path("<str:username>", views.UserNameReview.as_view()),
    path("<int:lectureId>", views.ReviewView.as_view()),
    path("<int:lectureId>/<int:reviewId>", views.ReplyView.as_view()),
]
