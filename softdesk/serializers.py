from rest_framework.serializers import ModelSerializer
from softdesk.models import Project,  Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["creator", "description", "name", "type", "status", "time_created", "modification_time"]


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["user", "project", "time_created"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["creator", "project", "assigned_user", "status", "type", "priority",
                  "title", "description", "time_created", "modification_time"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["creator", "related_issue", "content", "time_created", "modification_time"]
