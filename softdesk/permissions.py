from rest_framework.permissions import BasePermission

from softdesk.models import Contributor


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


class ContributorPostPermission(UserPermission):
    # todo à supprimer probablement
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            contributor = Contributor.objects.filter(user=request.user, project=request.kwargs["project_pk"])
            return len(contributor) > 0 and super().has_object_permission(request, view, obj)


