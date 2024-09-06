from rest_framework.serializers import ModelSerializer
from softdesk.models import Project, Contributor, Issue, Comment


class ContributorSerializer(ModelSerializer):
    def create(self, validated_data):
        # todo possibilité de récupérer l'id de project via l'url ??
        contributor = Contributor.objects.create(user=validated_data["user"],
                                                 project=validated_data["project"]
                                                 )
        return contributor

    class Meta:
        model = Contributor
        fields = ["user", "project", "time_created"]


class ProjectSerializer(ModelSerializer):
    def create(self, validated_data):
        project = Project.objects.create(creator=validated_data["creator"],
                                         description=validated_data["description"],
                                         name=validated_data["name"],
                                         type=validated_data["type"],
                                         status=validated_data["status"],
                                         )
        return project

    class Meta:
        model = Project
        fields = ["creator", "description", "name", "type", "status", "time_created", "modification_time",
                  "contributors"]

    contributors = ContributorSerializer(many=True, read_only=True)


class CommentSerializer(ModelSerializer):
    def create(self, validated_data):
        # todo possibilité de récupérer l'id de l'issue via l'url ??
        comment = Comment.objects.create(creator=validated_data["creator"],
                                         related_issue=validated_data["related_issue"],
                                         content=validated_data["content"])
        return comment

    class Meta:
        model = Comment
        fields = ["creator", "related_issue", "content", "time_created", "modification_time"]


class IssueSerializer(ModelSerializer):
    def create(self, validated_data):
        # todo possibilité de récupérer l'id de project via l'url ??
        issue = Issue.objects.create(creator=validated_data["creator"],
                                     project=validated_data["project"],
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
        fields = ["creator", "assigned_user", "project", "status", "type", "priority",
                  "title", "description", "time_created", "modification_time"]

        comments = CommentSerializer(many=True, read_only=True)

        def to_representation(self):
            pass
