from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is "GET":
            return True

        return obj.user == request.user


class CreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is "GET":
            return True

        return obj.creator == request.user

