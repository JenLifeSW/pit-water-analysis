from rest_framework.permissions import IsAuthenticated


class IsAdminRole(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.user.role == "admin")


class IsPostAble(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return super().has_permission(request, view)
