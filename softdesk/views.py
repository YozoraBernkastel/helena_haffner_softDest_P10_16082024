from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from softdesk.permissions import AuthorPermission, ProjectPermission, ContributorPermission, GateKeeper
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import (ProjectSerializer, ProjectListSerializer, ContributorSerializer,
                                  ContributorListSerializer, IssueSerializer, IssueListSerializer,
                                  CommentSerializer, CommentListSerializer)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes: list = [ContributorPermission]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        return project.contributors.all()

    def get_serializer_class(self):
        if "pk" not in self.kwargs:
            self.serializer_class = ContributorListSerializer

        return super().get_serializer_class()


class ProjectsViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes: list = [ProjectPermission]

    def get_serializer_class(self):
        if "pk" not in self.kwargs:
            self.serializer_class = ProjectListSerializer

        return super().get_serializer_class()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes: list = [AuthorPermission]

    def get_queryset(self):
        issues = None
        project = self.kwargs["project_pk"]
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issues = Issue.objects.filter(project=project)

        return issues

    def get_serializer_class(self):
        if "pk" not in self.kwargs:
            self.serializer_class = IssueListSerializer

        return super().get_serializer_class()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes: list = [AuthorPermission]

    def get_queryset(self):
        issue = None
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])

        return issue.comments.all()

    def get_serializer_class(self):
        if "pk" not in self.kwargs:
            self.serializer_class = CommentListSerializer

        return super().get_serializer_class()


# Creation views
class ProjectCreationViewset(CreateAPIView):
    model = Project
    serializer_class = ProjectSerializer


class ContributorCreationViewset(ModelViewSet, GateKeeper):
    model = Contributor
    serializer_class = ContributorSerializer

    def create(self, request, *args, **kwargs):
        if self.is_authorized_to_create(request, kwargs):
            return super().create(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)


class IssueCreationVieweset(ModelViewSet, GateKeeper):
    model = Issue
    serializer_class = IssueSerializer

    def create(self, request, *args, **kwargs):
        if self.is_authorized_to_create(request, kwargs):
            return super().create(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentCreationViewset(ModelViewSet, GateKeeper):
    model = Comment
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        if self.is_part_of_the_project(request.user, kwargs["project_pk"]):
            return super().create(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)
