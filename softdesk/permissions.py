from rest_framework.permissions import BasePermission
from softdesk.models import Contributor, Project


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.user == request.user


class CreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.creator == request.user


class ProjectPermission(CreatorPermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            contributor = Contributor.objects.filter(user=request.user, project=obj)

            return len(contributor) > 0 and super().has_object_permission(request, view, obj)

        return super().has_object_permission(request, view, obj)


class ContributorPermission(UserPermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            contributor = Contributor.objects.filter(user=request.user, project=obj.project)

            return len(contributor) > 0 and super().has_object_permission(request, view, obj)

        return super().has_object_permission(request, view, obj)


class GateKeeper:
    @staticmethod
    def is_creator(user, project_pk) -> bool:
        creator = Project.objects.filter(pk=project_pk, creator=user)
        return len(creator) > 0

    @staticmethod
    def is_contributor(user, project_pk) -> bool:
        contributor = Contributor.objects.filter(user=user, project=project_pk)
        return len(contributor) > 0

    def is_part_of_the_project(self, user, project_pk) -> bool:
        return self.is_creator(user, project_pk) or self.is_contributor(user, project_pk)

    @staticmethod
    def is_same_project(request, kwargs: dict) -> bool:
        return request.data["project"] == kwargs["project_pk"]

    def is_authorized_to_create(self, request, kwargs: dict) -> bool:
        return self.is_same_project(request, kwargs) and self.is_part_of_the_project(request.user, kwargs["project_pk"])
