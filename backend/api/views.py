from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     GenericAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated, ValidationError
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

    @action(detail=True)
    def submissions(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_object()
        serializer = serializers.SubmissionSerializer(
            form.submissions.all().order_by('-timestamp'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFormView(RetrieveAPIView):
    serializer_class = serializers.UserFormSerializer
    queryset = models.Form.objects.all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_object()

        if form.closed or form.time_is_out:
            # Maybe it's better to use 403 in this case
            return Response({'title': form.title}, status=status.HTTP_410_GONE)

        serializer = self.serializer_class(form)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSubmitFormView(GenericAPIView):
    queryset = models.Form.objects.all()

    def post(self, request: Request, *args, **kwargs) -> Response:
        if 'answers' not in request.data:
            raise ValidationError("Request body must contain 'answers' field")

        form = self.get_object()
        # Check if form is closed
        if form.closed or form.time_is_out:
            # Maybe it's better to use 403 in this case
            return Response({'title': form.title}, status=status.HTTP_410_GONE)

        answers_dict = [
            {'question': k, 'text': v}
            for k, v in request.data['answers'].items()
        ]

        required_questions = form.questions.filter(required=True)

        # Check if every required question is answered
        required_questions_ids_set = set(list(
            map(str, required_questions.values_list('id', flat=True))
        ))
        present_question_ids_set = set(request.data['answers'].keys())

        if len(required_questions_ids_set - present_question_ids_set) != 0:
            raise ValidationError("Every required question must be answered")

        # Serialize questions
        answers_serializer = serializers.CreateAnswerSerializer(
            data=answers_dict, many=True)
        answers_serializer.is_valid(raise_exception=True)

        submission = models.Submission.objects.create(form=form)

        answer_instances = [
            models.Answer(**data, submission=submission)
            for data in answers_serializer.validated_data
        ]

        answers = models.Answer.objects.bulk_create(answer_instances)
        submission.answers.set(answers)

        return Response(status=status.HTTP_201_CREATED)
