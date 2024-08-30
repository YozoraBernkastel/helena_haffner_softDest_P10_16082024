from rest_framework.viewsets import ReadOnlyModelViewSet

from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class ProjectsViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ContributorsViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        contributors = None
        project = self.request.GET.get("project")

        if project is not None:
            contributors = Contributor.objects.filter(project=project)

        return contributors


class IssueViewset(ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        issues = None
        project = self.request.GET.get("project")
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issues = Issue.objects.filter(project=project)

        return issues


class CommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):

        comments = None
        project = self.request.GET.get("project")
        user_as_contributor = Contributor.objects.filter(user=self.request.user, project=project)

        if project is not None and user_as_contributor is not None:
            issue = self.request.GET.get("issue")
            print(f"{issue = }")
            comments = Comment.objects.filter(related_issue=issue)

        return comments
