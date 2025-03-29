from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotAuthenticated
from rest_framework import status

from django.conf import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        original_resp = super().post(request, *args, **kwargs)

        if 'access' in original_resp.data and 'refresh' in original_resp.data:
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token', value=original_resp.data['access'],
                httponly=True, secure=settings.HTTPS, samesite='none',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            )
            response.set_cookie(
                key='refresh_token', value=original_resp.data['refresh'],
                httponly=True, secure=settings.HTTPS, samesite='none',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            )
            return response

        return original_resp


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh_token', None)
        if refresh_token is None:
            raise NotAuthenticated
        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token', value=serializer.validated_data['access'],
            httponly=True, secure=True, samesite='lax',
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )

        return response


class LogoutView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
