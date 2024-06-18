from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.users.models import User


class UserInfoSerializer(BaseSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nickname", "email", "phone", "role_name"]

    def get_role_name(self, obj):
        return obj.role.name
