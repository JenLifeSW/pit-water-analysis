from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.common.regex_string import regex_str_hatchery_name, regex_str_hatchery_description
from pit_api.hatcheries.models import Hatchery
from pit_api.hatcheries.validators import HatcheryNameValidator, HatcheryDescriptionValidator, HatcheryAddressValidator
from pit_api.tanks.serializers import TankInfoSerializer


class HatcherySerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail", "image"]

    name = serializers.CharField(
        required=True,
        min_length=2,
        validators=[HatcheryNameValidator()],
        help_text=regex_str_hatchery_name
    )
    description = serializers.CharField(
        required=False,
        validators=[HatcheryDescriptionValidator()],
        help_text=regex_str_hatchery_description
    )
    address = serializers.CharField(
        required=False,
        validators=[HatcheryAddressValidator()],
        help_text=regex_str_hatchery_description
    )
    addressDetail = serializers.CharField(
        source='address_detail',
        required=False,
        validators=[HatcheryAddressValidator()],
        help_text=regex_str_hatchery_description
    )
    image = serializers.SerializerMethodField(
        required=False
    )

    def get_image(self, obj):
        return ""


class HatcheryDetailSerializer(BaseSerializer):
    class Meta:
        model = Hatchery
        fields = ["id", "name", "description", "address", "addressDetail", "tanks", "image"]

    addressDetail = serializers.CharField(source='address_detail', required=False)
    tanks = TankInfoSerializer(many=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return ""
