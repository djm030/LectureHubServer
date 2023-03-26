from django.urls import path
from . import views

urlpatterns = [
    path("all/all/", views.Lectures.as_view()),
    path("<int:pk>", views.LecturesDetail.as_view()),
    path("search", views.SearchLectures.as_view()),
    path("<str:category1>/all/", views.OneCategory.as_view()),
    path("<str:category1>/all/<int:pages>", views.OneCategoryPage.as_view()),
    path("<str:category1>/<str:category2>/", views.TwoCategory.as_view()),
    path(
        "<str:category1>/<str:category2>/<int:pages>", views.TwoCategoryPage.as_view()
    ),
    path("@<str:username>", views.InstructorName.as_view()),
    path("mainpage", views.MainPage.as_view()),
]
