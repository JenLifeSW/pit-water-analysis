from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.hatcheries.models import Hatchery
from pit_api.hatcheries.validators import HatcheryNameValidator, HatcheryDescriptionValidator, HatcheryAddressValidator
from pit_api.tanks.serializers import TankInfoSerializer


class HatcherySerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail"]

    name = serializers.CharField(required=True, min_length=2, validators=[HatcheryNameValidator()])
    description = serializers.CharField(required=False, validators=[HatcheryDescriptionValidator()])
    address = serializers.CharField(required=False, validators=[HatcheryAddressValidator()])
    addressDetail = serializers.CharField(source='address_detail', required=False,
                                          validators=[HatcheryAddressValidator()])


class HatcheryDetailSerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail", "tanks"]

    addressDetail = serializers.CharField(source='address_detail', required=False)
    tanks = TankInfoSerializer(many=True)
