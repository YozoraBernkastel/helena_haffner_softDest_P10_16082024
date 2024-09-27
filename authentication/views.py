from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer


class SignupView(CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes: list = []


class DeleteViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        if int(self.kwargs["pk"]) == self.request.user.pk or self.request.user.is_superuser:
            return get_object_or_404(User, pk=int(self.kwargs["pk"]))

