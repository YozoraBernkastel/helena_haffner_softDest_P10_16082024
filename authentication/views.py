from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import CreateUserSerializer, UserSerializer


class SignupView(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer
    permission_classes: list = []


class DeleteViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

