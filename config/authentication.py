from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
import jwt
from django.conf import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        id = decoded.get("id")
        username = decoded.get("username")
        if not id or not username:
            raise AuthenticationFailed("Invalid Token")
        print(decoded)
        try:
            user = User.objects.get(username=username)
            print(user)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("user no found")
