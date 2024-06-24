from rest_framework.permissions import IsAuthenticated


class BaseRolePermission(IsAuthenticated):
    allowed_roles = []

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        return request.user.role.name in self.allowed_roles


class IsUserRole(BaseRolePermission):
    allowed_roles = ["user", "manager", "admin", "operator"]


class IsManagerRole(BaseRolePermission):
    allowed_roles = ["manager", "admin", "operator"]


class IsAdminRole(BaseRolePermission):
    allowed_roles = ["admin", "operator"]


class IsOperatorRole(BaseRolePermission):
    allowed_roles = ["operator"]
