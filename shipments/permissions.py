from rest_framework import permissions


class IsAuthenticatedForWriteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # (GET، HEAD، OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # (POST، PUT، DELETE).
        return request.user and request.user.is_authenticated
