from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from softdesk.permissions import CreatorPermission, ProjectPermission, ContributorPermission, ContributorPostPermission
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from softdesk.custom_pagination import CustomPagination


# todo il faudra penser à paginer certaines requêtes (ça fait parti du projet)

class ProjectsViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes: list = [ProjectPermission]
    pagination_class = CustomPagination


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes: list = [ContributorPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        return project.contributors.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes: list = [CreatorPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        issues = None
        project = self.kwargs["project_pk"]
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issues = Issue.objects.filter(project=project)

        return issues


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes: list = [CreatorPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        issue = None
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])

        return issue.comments.all()


# Creation views
class ProjectCreationViewset(CreateAPIView):
    model = Project
    serializer_class = ProjectSerializer


class ContributorCreationViewset(ModelViewSet):
    model = Contributor
    # todo des restrictions ? Peut-être qu'il faut vérifier si l'utilisateur qui crée le contributeur est lui-même contributeur/ créateur du projet ?
    serializer_class = ContributorSerializer


class IssueCreationVieweset(ModelViewSet):
    model = Issue
    serializer_class = IssueSerializer
    # todo ne fonctionne pas !!!
    permission_classes: list = [ContributorPostPermission]


class CommentCreationViewset(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    # todo ne fonctionne pas !!!
    permission_classes: list = [ContributorPostPermission]

