from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework.permissions import BasePermission
from softdesk.models import Contributor, Project


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.user == request.user


class AuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.author.user == request.user


class ProjectPermission(AuthorPermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return Contributor.objects.filter(user=request.user, project=obj).exists()

        return super().has_object_permission(request, view, obj)


class ContributorPermission(UserPermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return Contributor.objects.filter(user=request.user, project=view.kwargs["project_pk"]).exists()
        return super().has_permission(request, view)


    def has_object_permission(self, request, view, obj):

        return  Contributor.objects.filter(user=request.user, project=obj.project).exists()

class InsideProjectPermission(BasePermission):

    def has_permission(self, request, view):
        return Contributor.objects.filter(user=request.user, project=view.kwargs["project_pk"]).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return  Contributor.objects.filter(user=request.user, project=obj.project).exists()

        return request.user == obj.author.user

class GateKeeper:
    @staticmethod
    def is_contributor(user, project_pk) -> bool:
        return get_object_or_404(Contributor, user=user, project=project_pk)

    # @staticmethod
    # def is_author(user, project_pk) -> bool:
    #     contributor = Contributor.objects.filter(user=user, project=project_pk)
    #     return contributor.exists() and Project.objects.filter(pk=project_pk, author=contributor[0]).exists()
