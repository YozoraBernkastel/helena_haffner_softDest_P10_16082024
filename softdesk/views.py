from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class ProjectsViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter()
        serializer = ProjectSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(client)
        return Response(serializer.data)


class ContributorsViewset(ReadOnlyModelViewSet):
    serializer_class = ContributorSerializer

    def list(self, request, project_pk=None):
        queryset = Contributor.objects.filter(client=project_pk)
        serializer = ContributorSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(pk=pk, project=project_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)

    # def get_queryset(self):
    #     contributors = None
    #     project = self.request.GET.get("project")
    #
    #     if project is not None:
    #         contributors = Contributor.objects.filter(project=project)
    #
    #     return contributors


class IssuesViewset(ReadOnlyModelViewSet):
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
