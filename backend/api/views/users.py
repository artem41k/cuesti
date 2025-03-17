from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api import serializers, models


class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.all()

    def get_object(self):
        return self.request.user
