from rest_framework import serializers

from . import models

# User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email']


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'password', 'email']

# Answer


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['question', 'text']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['id', 'question', 'text']

# Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'title', 'description', 'form',
                  'question_type', 'required',
                  'max_length', 'min_value', 'max_value',
                  'regex', 'choices']

# Form


class ShortFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = ['id', 'title', 'description', 'owner',
                  'deadline', 'closed']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Form
        fields = ['id', 'title', 'description', 'owner',
                  'questions', 'questions_order',
                  'deadline', 'closed']

# Submission


class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Submission
        fields = ['id', 'form', 'answers', 'timestamp']
