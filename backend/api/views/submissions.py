from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from api import serializers, models


class SubmissionView(RetrieveAPIView):
    serializer_class = serializers.SubmissionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Submission.objects.filter(form__owner=self.request.user)
