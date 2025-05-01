from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.signing import b62_encode
from datetime import datetime
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = b62_encode(uuid.uuid4().int)
        super().save(*args, **kwargs)

    @property
    def time_is_out(self) -> bool:
        now = datetime.now()
        if self.deadline is None or now < self.deadline:
            return False
        return True

    def __str__(self):
        return self.title


class Question(models.Model):
    class Types(models.TextChoices):
        TEXT = 'text'
        NUMBER = 'number'
        COLOR = 'color'
        CHOICE = 'choice'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=200, blank=True)
    form = models.ForeignKey(
        to=Form, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=32, blank=False, choices=Types.choices)
    required = models.BooleanField(blank=False)

    # Text
    max_length = models.PositiveIntegerField(null=True)
    # Text & Color
    regex = models.CharField(max_length=256, null=True)
    # Numbers
    max_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)
    is_float = models.BooleanField(null=True)
    # Choices
    choices = models.JSONField(null=True)


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    form = models.ForeignKey(
        to=Form, related_name='submissions', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.ForeignKey(
        to=Question, related_name='answers', on_delete=models.CASCADE)
    submission = models.ForeignKey(
        to=Submission, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
