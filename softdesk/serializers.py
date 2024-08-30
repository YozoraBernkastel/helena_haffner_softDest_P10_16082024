from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, HyperlinkedIdentityField
from softdesk.models import Project,  Contributor, Issue, Comment
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class ProjectContributorSerializer(NestedHyperlinkedRelatedField):
    parent_lookup_kwargs = {
        "project_pk": "project__pk"
    }

    class Meta:
        model = Contributor
        fields = ["user", "project", "time_created"]


class ProjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Project
        lookup_field = "pk"
        contributors = HyperlinkedIdentityField(view_name="contributors", lookup_url_kwarg="project_pk")
        lookup_url_kwarg = 'project_pk'
        fields = ["creator", "description", "name", "type", "status", "time_created", "modification_time", "contributor"]

    contributor = ProjectContributorSerializer(view_name="contributors", many=True, read_only=True)


class ContributorSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Contributor
        lookup_url_kwarg = 'contributor_pk'
        fields = ["user", "project", "time_created"]


class IssueSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        lookup_url_kwarg = 'issue_pk'
        fields = ["creator", "project", "assigned_user", "status", "type", "priority",
                  "title", "description", "time_created", "modification_time"]


class CommentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        # lookup_url_kwarg = 'comment_pk'
        fields = ["creator", "related_issue", "content", "time_created", "modification_time"]
