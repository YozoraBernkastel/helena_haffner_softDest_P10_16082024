from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from softdesk.permissions import ProjectPermission, ContributorPermission, InsideProjectPermission, GateKeeper
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import (ProjectSerializer, ProjectListSerializer, ContributorSerializer,
                                  ContributorListSerializer, IssueSerializer, IssueListSerializer,
                                  CommentSerializer, CommentListSerializer)


class ContributorViewset(ModelViewSet, GateKeeper):
    serializer_class = ContributorSerializer
    permission_classes: list = [ContributorPermission]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        return project.contributors.all()

    def get_serializer_class(self):
        if "pk" not in self.kwargs:
            self.serializer_class = ContributorListSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(user=self.request.user, project=project)


class ProjectsViewset(ModelViewSet, GateKeeper):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes: list = [ProjectPermission]

    @staticmethod
    def is_new_author_contributor(data, project_pk) -> bool:
        return not "author" in data or Contributor.objects.filter(pk=data["author"], project=project_pk).exists()

    def partial_update(self, request, *args, **kwargs):
        if self.is_new_author_contributor(request.data, kwargs["pk"]):
            return super().partial_update(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        if self.action == "list":
            self.serializer_class = ProjectListSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        contributor = Contributor.objects.create(user=self.request.user, project=None)
        project = serializer.save(author=contributor)
        contributor.project = project
        contributor.save()


class IssueViewset(ModelViewSet, GateKeeper):
    serializer_class = IssueSerializer
    permission_classes: list = [InsideProjectPermission]

    def get_queryset(self):
        issues = None
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issues = Issue.objects.filter(project=project)

        return issues

    def get_serializer_class(self):
        if self.action == "list":
            self.serializer_class = IssueListSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if self.is_contributor(request.user, kwargs["project_pk"]):
            return super().create(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        contributor = get_object_or_404(Contributor, user=self.request.user, project=project)
        serializer.save(author=contributor, project=project)


class CommentViewset(ModelViewSet, GateKeeper):
    serializer_class = CommentSerializer
    permission_classes: list = [InsideProjectPermission]

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

    def create(self, request, *args, **kwargs):
        if self.is_contributor(request.user, kwargs["project_pk"]):
            return super().create(request, args, kwargs)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        contributor = get_object_or_404(Contributor, user=self.request.user, project=project)
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])
        serializer.save(author=contributor, related_issue=issue)
