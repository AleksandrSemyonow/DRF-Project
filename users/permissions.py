from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Доступно модераторам'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = "Доступно только владельцу"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
