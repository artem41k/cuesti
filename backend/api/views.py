from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.shortcuts import get_object_or_404
from django.conf import settings

from . import serializers, models


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


class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.all()

    def get_object(self):
        return self.request.user


class ManageFormViewSet(ModelViewSet):
    serializer_class = serializers.FormSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Form.objects.filter(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def update_questions(self, request: Request, *args, **kwargs) -> Response:
        for pk, changes in request.data.items():
            question = get_object_or_404(models.Question, pk=pk)
            q_serializer = serializers.QuestionSerializer(
                instance=question, data=changes, partial=True)
            q_serializer.is_valid(raise_exception=True)
            q_serializer.save()

        form = self.get_object()
        serializer = self.serializer_class(instance=form)

        return Response(serializer.data, status=status.HTTP_200_OK)
