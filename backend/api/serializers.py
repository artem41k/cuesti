from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        extra_kwargs = {
            'form': {'required': False}
        }

    def validate(self, attrs: dict):
        BANNED_FIELDS = {
            'text': {'max_value', 'min_value', 'regex', 'choices'},
            'number': {'max_length', 'regex', 'choices'},
            'color': {
                'max_length', 'max_value', 'min_value', 'regex', 'choices'},
            'choices': {'max_length', 'max_value', 'min_value', 'regex'},
            'regex': {'max_length', 'max_value', 'min_value', 'choices'},
        }
        if self.instance:
            question_type = self.instance.question_type
        else:
            question_type = attrs['question_type']
        banned_in_attrs = set(BANNED_FIELDS[question_type]) & set(attrs)

        if len(banned_in_attrs) != 0:
            raise ValidationError(
                'Incorrect fields for question with type %s were given: %s'
                % (question_type, ', '.join(banned_in_attrs)))

        return super().validate(attrs)

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
        fields = ['id', 'title', 'description', 'questions',
                  'questions_order', 'deadline', 'closed']

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
        questions: list[models.Question] = validated_data.pop('questions')
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

# Submission


class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Submission
        fields = ['id', 'form', 'answers', 'timestamp']
