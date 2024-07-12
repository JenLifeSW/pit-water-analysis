from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.common.regex_string import regex_str_hatchery_name, regex_str_hatchery_description
from pit_api.fish_species.models import FishSpecies
from pit_api.measurements.models import MeasurementData, TankTargetAssociation
from pit_api.measurements.serializers import MeasurementDataSerializer, MeasurementTargetSerializer
from pit_api.tanks.models import Tank
from pit_api.tanks.validators import TankNameValidator, TankDescriptionValidator


class TankSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "fishSpeciesId", "description"]

    name = serializers.CharField(
        required=True,
        min_length=2,
        validators=[TankNameValidator()],
        help_text=regex_str_hatchery_name
    )
    description = serializers.CharField(
        required=False,
        validators=[TankDescriptionValidator()],
        help_text=regex_str_hatchery_description
    )
    fishSpeciesId = serializers.PrimaryKeyRelatedField(queryset=FishSpecies.objects.all(), source="fish_species")


class TankInfoSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "description", "fishSpecies", "measurementTargets", "lastMeasuredAt"]

    fishSpecies = serializers.SerializerMethodField()
    measurementTargets = serializers.SerializerMethodField()
    lastMeasuredAt = serializers.SerializerMethodField()

    def get_fishSpecies(self, obj):
        fish_species = obj.fish_species
        return {
            "id": fish_species.id,
            "name": fish_species.name
        }

    def get_measurementTargets(self, obj):
        targets = TankTargetAssociation.objects.filter(tank=obj).select_related('target')
        return MeasurementTargetSerializer([association.target for association in targets], many=True).data

    def get_lastMeasuredAt(self, obj):
        tank_target_associations = TankTargetAssociation.objects.filter(tank=obj)
        latest_measurement = MeasurementData.objects.filter(tank_target__in=tank_target_associations).order_by(
            '-measured_at').first()
        return latest_measurement.measured_at if latest_measurement else None


class TankDetailSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "description", "fishSpecies", "measurementDatas"]

    fishSpecies = serializers.SerializerMethodField()
    measurementDatas = serializers.SerializerMethodField()

    def get_fishSpecies(self, obj):
        fish_species = obj.fish_species
        return {
            "id": fish_species.id,
            "name": fish_species.name
        }

    def get_measurementDatas(self, obj):
        tank_targets = TankTargetAssociation.objects.filter(tank=obj).select_related('target')

        measurement_datas = []
        for tank_target in tank_targets:
            latest_measurement = MeasurementData.objects.filter(tank_target=tank_target).order_by(
                '-measured_at').first()

            if latest_measurement:
                measurement_datas.append(latest_measurement)
            else:
                measurement_datas.append(MeasurementData(
                    tank_target=tank_target,
                    value=None,
                    measured_at=None
                ))

        return MeasurementDataSerializer(measurement_datas, many=True).data
