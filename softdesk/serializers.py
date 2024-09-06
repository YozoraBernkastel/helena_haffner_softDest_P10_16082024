from rest_framework.serializers import ModelSerializer
from softdesk.models import Project,  Contributor, Issue, Comment


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["user", "time_created"]


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["creator", "description", "name", "type", "status", "time_created", "modification_time", "contributors"]

    contributors = ContributorSerializer(many=True, read_only=True)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["creator", "content", "time_created", "modification_time"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["creator", "assigned_user", "status", "type", "priority",
                  "title", "description", "time_created", "modification_time"]

        comments = CommentSerializer(many=True, read_only=True)

        def to_representation(self):
            pass

