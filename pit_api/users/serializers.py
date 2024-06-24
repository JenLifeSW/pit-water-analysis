from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.hatcheries.models import HatcheryManagerAssociation
from pit_api.users.models import User


class UserInfoSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "email", "phone", "role", "hatcheryIds"]

    role = serializers.SerializerMethodField()
    hatcheryIds = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.role.description

    def get_hatcheryIds(self, obj):
        return HatcheryManagerAssociation.objects.filter(user=obj).values_list('hatchery_id', flat=True)
