from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Form, Submission, Question, Answer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('last_login', 'date_joined')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ('id', 'title', 'question_type', 'required')
    readonly_fields = ('id',)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'closed', 'created_at')
    search_fields = ('id', 'title')
    list_filter = ('created_at', 'owner', 'closed')
    fields = ('id', 'owner', 'title', 'description',
              'deadline', 'closed', 'created_at')
    readonly_fields = ('id', 'owner', 'created_at')

    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'form', 'question_type')
    search_fields = ('id', 'title')
    list_filter = ('form', 'question_type')
    ordering = ('form',)
    fields = ('id', 'form', 'title', 'description',
              'question_type', 'required')
    readonly_fields = ('id', 'form')


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ('question_title', 'question_type', 'text')
    readonly_fields = ('question_title', 'question_type', 'text')

    def question_title(self, obj: Answer):
        return obj.question.title
    question_title.short_description = 'Question'

    def question_type(self, obj: Answer):
        return obj.question.question_type
    question_type.short_description = 'Question Type'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'timestamp')
    search_fields = ('id', 'form__title')
    list_filter = ('form', 'timestamp')
    ordering = ('-timestamp',)
    fields = ('id', 'form', 'timestamp')
    readonly_fields = ('id', 'form', 'timestamp')

    inlines = [AnswerInline]
