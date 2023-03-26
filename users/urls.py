from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("myprofile", views.UserProfileView.as_view()),
    path("user_password_change", views.UserPasswordView.as_view()),
    path("activite", views.ActiviteView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("@<str:username>", views.UsernameView.as_view()),
    path("jwttoken", views.JWTokenView.as_view()),
    path("instructor", views.AddInstructor.as_view()),
    path(
        "calculated-lectures/<int:lectureId>/", views.AddCalculateLecturesView.as_view()
    ),
    path(
        "jwt-token-auth/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # 로그인
    path(
        "jwt-token-auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 리프레시=> 액세스
    path(
        "jwt-token-auth/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),  # 유저인증
    path("test", views.UsertempProfileView.as_view()),  ## 테스트용
]
################################
# url list
# api/v1/users/ post : 회원가입
# api/v1/users/myprofile : get : 정보 조회 put : 정보 수정
# api/v1/users/user_password_change put : 비밀번호 변경
# api/v1/users/login post: 로그인
# api/v1/users/logout post: 로그아웃
# api/v1/users/@<str:username> get : 아이디 중복체크
################################
