from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import CreateUserSerializer, UserSerializer
from softdesk.models import Project


class SignupView(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer
    permission_classes: list = []


class DeleteViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def is_user_author_of_projects(self) -> bool:
        return Project.objects.filter(author__user=self.request.user).exists()

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        if self.is_user_author_of_projects():
            return Response(data={"error": "Impossible de supprimer car auteur de projet."},
                            status=status.HTTP_400_BAD_REQUEST)

        return self.destroy(request, *args, **kwargs)
