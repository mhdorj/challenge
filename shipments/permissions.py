from rest_framework import permissions


class IsAuthenticatedForWriteOnly(permissions.BasePermission):
    """
    اجازه برای همه به جز نوشتن و حذف کردن، که نیاز به احراز هویت دارد.
    """
    def has_permission(self, request, view):
        # اجازه دسترسی به همه برای خواندن (GET، HEAD، OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # فقط کاربر احراز هویت شده می‌تواند عملیات نوشتن (POST، PUT، DELETE) انجام دهد.
        return request.user and request.user.is_authenticated