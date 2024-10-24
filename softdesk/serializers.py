from rest_framework.serializers import ModelSerializer
from authentication.models import User
from authentication.serializers import UserSerializer
from softdesk.models import Project, Contributor, Issue, Comment


class DataRepresentation:
    @staticmethod
    def user_info(user: User) -> dict:
        return {"pk": user.pk, "username": user.username}

    @staticmethod
    def detail_user_info(user: User) -> dict:
        return {"pk": user.pk, "user": UserSerializer(user).data}

    @staticmethod
    def issue_info(issue: Issue) -> dict:
        return {"pk": issue.pk, "title": issue.title}


class ContributorSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = self.detail_user_info(instance.user)
        return response

    class Meta:
        model = Contributor
        fields = ["user", "time_created"]


class ContributorListSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = self.user_info( instance.user)
        return response

    class Meta:
        model = Contributor
        read_only_fields = ("user", "project",)
        fields = ["user"]


class ProjectSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_user_info(instance.author.user)
        return response

    class Meta:
        model = Project
        fields = [ "name", "author", "description", "type", "time_created", "modification_time",
                  "contributors"]

    contributors = ContributorListSerializer(many=True, read_only=True)


class ProjectListSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.user_info(instance.author.user)
        return response

    class Meta:
        model = Project
        read_only_fields= ("author",)
        fields = ["name", "author", "description", "type"]


class CommentSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_user_info(instance.author.user)
        return response

    class Meta:
        model = Comment
        read_only_fields = ("author", "related_issue",)
        fields = ["author", "content", "time_created", "modification_time"]


class CommentListSerializer(ModelSerializer, DataRepresentation):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.user_info(instance.author.user)
        response["related_issue"] = self.issue_info(instance.related_issue)
        return response

    class Meta:
        model = Comment
        read_only_fields = ("author", "related_issue",)
        fields = ["author", "content"]


class IssueSerializer(ModelSerializer, DataRepresentation):
    comments = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_user_info(instance.author.user)
        response["assigned_user"] = self.detail_user_info(instance.assigned_user.user)
        return response

    class Meta:
        model = Issue
        read_only_fields = ("author", "project")
        fields = ["author", "assigned_user", "status", "type", "priority",
                  "title", "description", "comments", "time_created", "modification_time"]

        comments = CommentSerializer(many=True, read_only=True)


class IssueListSerializer(ModelSerializer, DataRepresentation):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.user_info(instance.author.user)
        response["assigned_user"] = self.user_info(instance.assigned_user.user)
        return response


    class Meta:
        model = Issue
        fields = ["author", "assigned_user", "status", "type", "priority",
                  "title"]

        comments = CommentSerializer(many=True, read_only=True)

