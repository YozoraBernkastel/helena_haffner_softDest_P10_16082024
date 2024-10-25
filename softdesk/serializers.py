from rest_framework.serializers import ModelSerializer
from authentication.serializers import UserSerializer
from softdesk.models import Project, Contributor, Issue, Comment


class DataRepresentation:
    @staticmethod
    def contributor_info(instance) -> dict:
        return {"contributor_pk": instance.pk,
                "user_pk": instance.user.pk,
                "username": instance.user.username} \
            if instance.user else {"user_pk": "no user", "username": "no username"}

    @staticmethod
    def detail_contributor_info(instance) -> dict:
        return {"contributor_pk": instance.pk,
                "user_pk": instance.user.pk,
                "user_data": UserSerializer(instance.user).data} \
            if instance.user else {"user_pk": "no user", "user": "no user"}

    @staticmethod
    def detail_user_info(user) -> dict:
        return {"user_pk": user.pk, "user_data": UserSerializer(user).data} if user \
            else {"user_pk": "no user", "user": "no user"}

    @staticmethod
    def count_comments(issue: Issue):
        return len(Comment.objects.filter(related_issue=issue))

    @staticmethod
    def count_issues(project: Project):
        return len(Issue.objects.filter(project=project))



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
        response["user"] = self.contributor_info(instance)
        return response

    class Meta:
        model = Contributor
        read_only_fields = ("user", "project",)
        fields = ["user"]


class ProjectSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_contributor_info(instance.author)
        response["issues_number"] = self.count_issues(instance)
        return response

    class Meta:
        model = Project
        read_only_fields = ("author",)
        fields = ["name", "author", "description", "type", "time_created", "modification_time",
                  "contributors"]

    contributors = ContributorListSerializer(many=True, read_only=True)


class ProjectListSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["project_pk"] = instance.pk
        response["author"] = self.contributor_info(instance.author)
        return response

    class Meta:
        model = Project
        read_only_fields = ("author",)
        fields = ["name", "author", "description", "type"]


class CommentSerializer(ModelSerializer, DataRepresentation):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_contributor_info(instance.author)
        return response

    class Meta:
        model = Comment
        read_only_fields = ("author", "related_issue",)
        fields = ["author", "content", "time_created", "modification_time"]


class CommentListSerializer(ModelSerializer, DataRepresentation):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.contributor_info(instance.author)
        response["comment_pk"] = instance.pk
        return response

    class Meta:
        model = Comment
        read_only_fields = ("author",)
        fields = ["author", "content"]


class IssueSerializer(ModelSerializer, DataRepresentation):
    comments = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = self.detail_contributor_info(instance.author)
        response["assigned_user"] = self.detail_contributor_info(instance.assigned_user)
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
        response["issue_pk"] = instance.pk
        response["author"] = self.contributor_info(instance.author)
        response["assigned_user"] = self.contributor_info(instance.assigned_user)
        response["comments_number"] = self.count_comments(instance)
        return response

    class Meta:
        model = Issue
        fields = ["author", "assigned_user", "status", "type", "priority",
                  "title"]

        comments = CommentSerializer(many=True, read_only=True)

