from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from . import models, serializers


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        original_resp = super().post(request, *args, **kwargs)

        if 'access' in original_resp.data and 'refresh' in original_resp.data:
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token', value=original_resp.data['access'],
                httponly=True, secure=True, samesite='lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            )
            response.set_cookie(
                key='refresh_token', value=original_resp.data['refresh'],
                httponly=True, secure=True, samesite='lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            )
            return response

        return original_resp


class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer


class FormView(ModelViewSet):
    serializer_class = serializers.FormSerializer
