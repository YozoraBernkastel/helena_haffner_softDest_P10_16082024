from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


# Read Only Views
class ProjectsViewset(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])

        return project.contributors.all()


class IssueViewset(ReadOnlyModelViewSet):
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


# Creation views
class ProjectCreationViewset(CreateAPIView):
    model = Project
    serializer_class = ProjectSerializer


class ContributorCreationViewset(ModelViewSet):
    model = Contributor
    serializer_class = ContributorSerializer


class IssueCreationVieweset(ModelViewSet):
    model = Issue
    serializer_class = IssueSerializer


class CommentCreationViewset(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer


# delete views
class DeleteProjectViewset(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # model = Project
    #
    # def get_object(self):
    #     project = get_object_or_404(Project, pk=self.kwargs["project"])
    #     return project
