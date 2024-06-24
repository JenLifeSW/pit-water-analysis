from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.hatcheries.models import Hatchery
from pit_api.tanks.serializers import TankInfoSerializer


class HatcherySerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail"]

    name = serializers.CharField(required=True)
    addressDetail = serializers.CharField(source='address_detail', required=False)

    def validate_name(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("양식장 이름을 입력하세요.")
        return value


class HatcheryDetailSerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail", "tanks"]

    addressDetail = serializers.CharField(source='address_detail', required=False)
    tanks = TankInfoSerializer(many=True)
