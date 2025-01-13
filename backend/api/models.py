from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.signing import b62_encode
import uuid


class User(AbstractUser):
    pass


class Form(models.Model):
    id = models.CharField(
        max_length=22, primary_key=True, editable=False)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=200, blank=True)
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='forms')
    deadline = models.DateTimeField(null=True)
    closed = models.BooleanField(default=False)
    questions_order = ArrayField(
        base_field=models.CharField(max_length=36), blank=True, default=list)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = b62_encode(uuid.uuid4().int)
        super().save(*args, **kwargs)


class Question(models.Model):
    class Types(models.TextChoices):
        TEXT = 'text'
        NUMBER = 'number'
        REGEX = 'regex'
        COLOR = 'color'
        CHOICE = 'choice'

    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=200, blank=True)
    form = models.ForeignKey(
        to=Form, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=32, blank=False, choices=Types.choices)
    required = models.BooleanField(blank=False)

    max_length = models.PositiveIntegerField(null=True)
    max_value = models.IntegerField(null=True)
    min_value = models.IntegerField(null=True)
    regex = models.CharField(max_length=256, null=True)
    choices = models.JSONField(null=True)


class Submission(models.Model):
    id = models.UUIDField(primary_key=True)
    form = models.ForeignKey(
        to=Form, related_name='submissions', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True)
    question = models.ForeignKey(
        to=Question, related_name='answers', on_delete=models.CASCADE)
    submission = models.ForeignKey(
        to=Submission, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
