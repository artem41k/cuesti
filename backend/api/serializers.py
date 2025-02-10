from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
import re

from . import models

# User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']

    def update(self, instance, validated_data):
        new_password = None
        if 'password' in validated_data:
            new_password = validated_data.pop('password')
        upd_user: models.User = super().update(instance, validated_data)

        if new_password:
            upd_user.set_password(new_password)
            upd_user.save()

        return upd_user


class CreateUserSerializer(UserSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

# Answer


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['question', 'text']

    def validate(self, attrs: dict):
        question = attrs['question']
        types = models.Question.Types
        text: str = attrs['text']

        match question.question_type:
            case types.TEXT:
                if question.max_length and len(text) > question.max_length:
                    raise ValidationError(
                        "Answer exceeds max length (%d > %d) (question_id: %s)"
                        % (len(text), question.max_length, question.id)
                    )
            case types.NUMBER:
                try:
                    if question.is_float:
                        text = text.replace(',', '.')
                        num = float(text)
                    else:
                        num = int(text)
                except ValueError:
                    raise ValidationError(
                        "'%s' is not a valid %s"
                        % (text, "float" if question.is_float else "integer")
                    )

                if question.max_value and num > question.max_value:
                    raise ValidationError(
                        (
                            "Value is greater than max value (%s > %s) "
                            "(question_id: %s)"
                        ) % (text, question.max_value, question.id)
                    )
                if question.min_value and num < question.min_value:
                    raise ValidationError(
                        (
                            "Value is lower than min value (%s < %s) "
                            "(question_id: %s)"
                        ) % (text, question.min_value, question.id)
                    )
            case types.REGEX:
                if not re.fullmatch(question.regex, text):
                    raise ValidationError("Invalid answer")
            case types.COLOR:
                if not re.fullmatch(question.regex, text):
                    raise ValidationError(settings.COLOR_REGEX)
            case types.CHOICE:
                if question.choices and text not in question.choices:
                    raise ValidationError(
                        "Answer is not in list of possible values")

        return super().validate(attrs)

# Question


class ShortQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'title', 'description', 'question_type']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'title', 'description', 'form',
                  'question_type', 'required',
                  'max_length', 'min_value', 'max_value',
                  'is_float', 'regex', 'choices']
        extra_kwargs = {
            'form': {'required': False}
        }

    def validate_min_and_max_values(self, attrs: dict):
        check = ('min_value', 'max_value')
        for attr in check:
            if attr not in attrs:
                continue
            text = attrs[attr].replace(',', '.')
            is_float = attrs['is_float'] if 'is_float' in attrs else False
            try:
                if is_float:
                    _ = float(text)
                else:
                    if '.' in text:
                        raise ValidationError(
                            "%s can't be float if expected answer is not"
                            % attr
                        )
                    _ = int(text)
            except ValueError:
                raise ValidationError(
                    "%s '%s' is not a valid %s"
                    % (attr, text, "float" if is_float else "number")
                )

    def validate(self, attrs: dict):
        TYPE_FIELDS = {
            'text': {'max_length'},
            'number': {'max_value', 'min_value', 'is_float'},
            'color': set(),
            'choices': {'choices'},
            'regex': {'regex'},
        }
        POSSIBLE_FIELDS = {
            'max_length', 'max_value', 'min_value', 'is_float',
            'regex', 'choices'
        }
        if self.instance:
            question_type = self.instance.question_type
        else:
            question_type = attrs['question_type']
        allowed_fields = set(TYPE_FIELDS[question_type])
        not_allowed = (attrs & POSSIBLE_FIELDS) - allowed_fields

        if len(not_allowed) != 0:
            raise ValidationError(
                'Incorrect fields for question with type %s were given: %s'
                % (question_type, ', '.join(not_allowed)))

        if question_type == 'number':
            self.validate_min_and_max_values(attrs)

        return super().validate(attrs)


class UserQuestionSerializer(serializers.ModelSerializer):
    """ Pretty much the same as QuestionSerializer,
    but w/o regex and form fields  """
    class Meta:
        model = models.Question
        fields = ['id', 'title', 'description', 'question_type',
                  'required', 'max_length', 'min_value',
                  'max_value', 'is_float', 'choices']

# Form


class ShortFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = ['id', 'title', 'description', 'deadline', 'closed']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    submission_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Form
        fields = ['id', 'title', 'description', 'questions',
                  'questions_order', 'deadline', 'closed',
                  'submission_count']

    def get_submission_count(self, obj: models.Form) -> int:
        return models.Submission.objects.filter(form=obj).count()

    def validate_questions(self, questions_json: dict):
        serializer = QuestionSerializer(data=questions_json, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def validate_questions_order(self, order: list[str]) -> list[str]:
        if not self.instance:
            raise ValidationError(
                "You can't pass this field while form is not created"
            )
        order_set = set(order)
        existing_ids_set = set(list(
            map(str,
                models.Question.objects.all().values_list('id', flat=True))
        ))

        if len(order) != len(order_set):
            raise ValidationError("Items are not unique")
        if len(order) != len(self.instance.questions.all()):
            raise ValidationError(
                "Number of items in this field must be "
                "equal to number of questions"
            )
        if len(order_set - existing_ids_set) != 0:
            raise ValidationError(
                "Some question ids in this field are not found"
            )
        return order

    def create(self, validated_data: dict) -> models.Form:
        validated_data['owner'] = self.context['request'].user
        questions: list[dict] = validated_data.pop('questions')
        form: models.Form = super().create(validated_data)

        question_instances = [
            models.Question(**data, form=form)
            for data in questions
        ]
        questions = models.Question.objects.bulk_create(question_instances)

        form.questions_order = [q.id for q in questions]

        form.questions.set(questions)

        return form

    # TO FIX: there is still an error "question with this id already exists",
    # it occurs earlier, than 'questions' validation, or call of method below
    def update(self, instance, validated_data):
        if 'questions' in validated_data:
            raise ValidationError(
                "You can't update questions while updating form. "
                "There is a separate method for these purposes"
            )
        return super().update(instance, validated_data)


class UserFormSerializer(serializers.ModelSerializer):
    questions = UserQuestionSerializer(many=True)

    class Meta:
        model = models.Form
        fields = ['id', 'title', 'description', 'questions', 'questions_order']

# Submission


class AnswerSerializer(CreateAnswerSerializer):
    question = ShortQuestionSerializer()


class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Submission
        fields = ['id', 'form', 'answers', 'timestamp']
