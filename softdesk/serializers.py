from http.client import responses

from rest_framework.serializers import ModelSerializer
from authentication.serializers import UserSerializer
from softdesk.models import Project, Contributor, Issue, Comment


class ContributorSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response

    class Meta:
        model = Contributor
        fields = ["user", "project", "time_created"]


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project"]


class ProjectSerializer(ModelSerializer):
    # def create(self, validated_data):
    #     project = Project.objects.create(author=validated_data["creator"],
    #                                      description=validated_data["description"],
    #                                      name=validated_data["name"],
    #                                      type=validated_data["type"]    #
    #                                      )
    #     return project

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = UserSerializer(instance.author).data
        return response

    class Meta:
        model = Project
        fields = ["author", "description", "name", "type", "status", "time_created", "modification_time",
                  "contributors"]

    contributors = ContributorSerializer(many=True, read_only=True)


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["author", "description", "name", "type", "status"]


class CommentSerializer(ModelSerializer):
    def create(self, validated_data):
        contributor = Contributor.objects.get(user=self._kwargs["pk"], project=self._kwargs["project_pk"])
        comment = Comment.objects.create(author=contributor,
                                         related_issue=validated_data["related_issue"],
                                         content=validated_data["content"])
        return comment

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = UserSerializer(instance.author).data
        return response

    class Meta:
        model = Comment
        fields = ["author", "related_issue", "content", "time_created", "modification_time"]


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["author", "related_issue", "content"]


class IssueSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        contributor = Contributor.objects.get(user=self._kwargs["pk"], project=self._kwargs["project_pk"])
        issue = Issue.objects.create(author=contributor,
                                     project=self._kwargs["project_pk"],
                                     assigned_user=validated_data["assigned_user"],
                                     status=validated_data["status"],
                                     type=validated_data["type"],
                                     priority=validated_data["priority"],
                                     title=validated_data["title"],
                                     description=validated_data["description"],
                                     )
        return issue

    class Meta:
        model = Issue
        fields = ["author", "assigned_user", "project", "status", "type", "priority",
                  "title", "description", "comments", "time_created", "modification_time"]

        comments = CommentSerializer(many=True, read_only=True)

        def to_representation(self):
            pass


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["author", "assigned_user", "project", "status", "type", "priority",
                  "title"]

        comments = CommentSerializer(many=True, read_only=True)

