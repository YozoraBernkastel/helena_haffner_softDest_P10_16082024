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


