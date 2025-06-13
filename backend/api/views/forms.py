from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from api import models, serializers, utils


class ManageFormViewSet(ModelViewSet):
    serializer_class = serializers.FormSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Form.objects.filter(
            owner=self.request.user).order_by('-created_at')

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

    @action(methods=['POST'], detail=True)
    def close(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_object()
        if not form.closed:
            form.closed = True
            form.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def submissions(self, request: Request, *args, **kwargs) -> Response:
        """ Returns all submissions like submission object """
        form = self.get_object()
        serializer = serializers.SubmissionSerializer(
            form.submissions.all().order_by('-timestamp'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def answers(self, request: Request, *args, **kwargs) -> Response:
        """ Returns list of questions with all their answers """
        form = self.get_object()
        serializer = serializers.QuestionAnswersSerializer(
            form.questions.all(), many=True)
        data = {}
        for question in serializer.data:
            data[question['id']] = question['answers']
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def excel(self, request: Request, *args, **kwargs) -> Response:
        """ Returns Excel table containing all submissions """
        form: models.Form = self.get_object()
        questions = form.questions.all()

        headers = ["ID"] + [
            q.title for q in questions] + ["Timestamp"]
        rows = []

        sub_data = form.submissions.all().prefetch_related('answers')

        for sub in sub_data:
            row = [str(sub.pk)]
            answers = {ans.question.pk: ans.text for ans in sub.answers.all()}
            print(f"{answers=}")
            for q in questions:
                row.append(answers.get(q.pk, ''))
            row += [str(sub.timestamp)]
            rows.append(row)

        excel_attachment = utils.to_excel_attachment(form.title, headers, rows)

        response = HttpResponse(
            excel_attachment,
            content_type='application/vnd.openxmlformats-'
            'officedocument.spreadsheetml.sheet'
        )
        filename = f'cuesti_{form.pk}.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


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
