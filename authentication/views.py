from rest_framework.generics import CreateAPIView
from authentication.models import User
from authentication.serializers import UserSerializer


class SignupView(CreateAPIView):
    model = User
    serializer_class = UserSerializer
