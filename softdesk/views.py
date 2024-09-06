from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class ProjectsViewset(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectCreationViewset(CreateAPIView):
    print("création de projet")
    model = Project
    serializer_class = ProjectSerializer


class ContributorsViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        return project.contributors.all()


class IssuesViewset(ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        issues = None
        project = self.kwargs["project_pk"]
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issues = Issue.objects.filter(project=project)

        return issues


class CommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):

        issue = None
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])

        return issue.comments.all()
